import requests
import pandas as pd
import json
from multiprocessing import Pool
import itertools
from .exceptions import NoMatchingDataError
from .parsers import parse_final_domain, parse_base_output
from typing import List, Dict
from .util import to_snake_case

__title__ = "jao-py"
__version__ = "0.3.13"
__author__ = "Frank Boerman"
__license__ = "MIT"


class JaoPublicationToolClient:
    BASEURL = "https://publicationtool.jao.eu/core/api/core/"
    BASEURL2 = "https://publicationtool.jao.eu/core/api/data/"

    def __init__(self, api_key: str = None):
        self.s = requests.Session()
        self.s.headers.update({
            'user-agent': 'jao-py (github.com/fboerman/jao-py)'
        })

        if api_key is not None:
            self.s.headers.update({
                'Authorization': 'Bearer ' + api_key
            })

    def _starmap_pull(self, url, params, keyname=None):
        r = self.s.get(url, params=params)
        r.raise_for_status()
        if keyname is not None:
            return r.json()[keyname]
        else:
            return r.json()

    def query_final_domain(self, mtu: pd.Timestamp, presolved: bool = None, cne: str = None, co: str = None,
                           urls_only: bool = False) -> List[Dict]:
        if type(mtu) != pd.Timestamp:
            raise Exception('Please use a timezoned pandas Timestamp object for mtu')
        if mtu.tzinfo is None:
            raise Exception('Please use a timezoned pandas Timestamp object for mtu')
        mtu = mtu.tz_convert('UTC')
        if cne is not None or co is not None or bool is not None:
            filter = {
                'cneName': "" if cne is None else cne,
                'contingency': "" if co is None else co,
                'presolved': presolved
            }
        else:
            filter = None

        # first do a call with zero retrieved data to know how much data is available, then pull all at once
        r = self.s.get(self.BASEURL + "finalComputation/index", params={
            'date': mtu.isoformat(),
            'search': json.dumps(filter),
            'skip': 0,
            'take': 0
        })
        r.raise_for_status()

        if r.json()['totalRowsWithFilter'] == 0:
            raise NoMatchingDataError

        # now do new call with all data requested
        # jao servers are not great returning it all at once, but they let you choose your own pagination
        # lets go for chunks of 5000, arbitrarily chosen

        total_num_data = r.json()['totalRowsWithFilter']
        args = []
        for i in range(0, total_num_data, 5000):
            args.append((self.BASEURL + "finalComputation/index", {
                'date': mtu.isoformat(),
                'search': json.dumps(filter),
                'skip': i,
                'take': 5000
            }, 'data'))

        if urls_only:
            return args

        with Pool() as pool:
            results = pool.starmap(self._starmap_pull, args)

        return list(itertools.chain(*results))

    def _query_base(self, day: pd.Timestamp, type: str) -> List[Dict]:
        r = self.s.get(self.BASEURL + type + '/index', params={
            'date': day.isoformat()
        })
        r.raise_for_status()
        data = r.json()[type]
        if len(data) == 0:
            raise NoMatchingDataError
        return data

    def _query_base_fromto(self, d_from: pd.Timestamp, d_to: pd.Timestamp, type: str) -> List[Dict]:
        r = self.s.get(self.BASEURL2 + type, params={
            'FromUTC': d_from.isoformat(),
            'ToUTC': d_to.isoformat()
        })
        r.raise_for_status()
        data = r.json()['data']
        if len(data) == 0:
            raise NoMatchingDataError
        return data

    def query_net_position(self, day: pd.Timestamp) -> List[Dict]:
        return self._query_base(day, 'netPos')

    def query_active_constraints(self, day: pd.Timestamp) -> List[Dict]:
        # although the same skip/take mechanism is active on this endpoint as the final domain, this is not needed to be used
        #   by definition active constraints are only a few so its overkill to start pagination
        # for the same reason this endpoint returns a whole day at once instead of per hour since there are not many
        #  and you probably want the whole day anyway
        # for the date range to be correct make sure the day input has a timezone!
        data = []
        for mtu in pd.date_range(day, day + pd.Timedelta(days=1), freq='1h'):
            r = self.s.get(self.BASEURL + 'shadowPrices/index', params={
                'date': mtu.isoformat()
            })
            r.raise_for_status()
            data += r.json()['data']
        if len(data) == 0:
            raise NoMatchingDataError

        return data

    def query_lta(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> List[Dict]:
        return self._query_base_fromto(d_from, d_to, 'lta')

    def query_validations(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> List[Dict]:
        return self._query_base_fromto(d_from, d_to, 'validationReductions')

    def query_maxbex(self, day: pd.Timestamp) -> List[Dict]:
        return self._query_base(day, 'maxExchanges')

    def query_minmax_np(self, day: pd.Timestamp) -> List[Dict]:
        return self._query_base(day, 'maxNetPos')

    def query_allocationconstraint(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> List[Dict]:
        return self._query_base_fromto(d_from, d_to, 'allocationConstraint')

    def query_status(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> List[Dict]:
        return self._query_base_fromto(d_from, d_to, 'spanningDefaultFBP')


class JaoPublicationToolPandasClient(JaoPublicationToolClient):
    def query_final_domain(self, mtu: pd.Timestamp, presolved: bool = None, cne: str = None,
                           co: str = None) -> pd.DataFrame:
        return parse_final_domain(
            super().query_final_domain(mtu=mtu, presolved=presolved, cne=cne, co=co)
        )

    def query_allocationconstraint(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        return parse_base_output(
            super().query_allocationconstraint(d_from=d_from, d_to=d_to)
        ).rename(columns=lambda c: c.split('_')[1] + '_' + ('import' if 'Down' in c.split('_')[0] else 'export'))

    def query_net_position(self, day: pd.Timestamp) -> pd.DataFrame:
        return parse_base_output(
            super().query_net_position(day=day)
        ).rename(columns=lambda x: x.replace('hub_', '')) \
            .rename(columns={'DE': 'DE_LU'})

    def query_active_constraints(self, day: pd.Timestamp) -> pd.DataFrame:
        return parse_base_output(
            super().query_active_constraints(day=day)
        ).rename(columns=lambda x: to_snake_case(x) if 'hub' not in x else x) \
            .rename(columns={'id': 'id_original'}) \
            .rename(columns=lambda x: x.replace('hub_', 'ptdf_'))

    def query_maxbex(self, day: pd.Timestamp, from_zone: str = None, to_zone: str = None) -> pd.DataFrame:
        df = parse_base_output(
            super().query_maxbex(day=day)
        ).rename(columns=lambda x: x.lstrip('border_').replace('_', '>'))

        if from_zone is not None:
            df = df[[c for c in df.columns if c.split('>')[0] == from_zone]]

        if to_zone is not None:
            df = df[[c for c in df.columns if c.split('>')[1] == to_zone]]

        return df

    def query_minmax_np(self, day: pd.Timestamp) -> pd.DataFrame:
        return parse_base_output(
            super().query_minmax_np(day=day)
        )

    def query_lta(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        return parse_base_output(
            super().query_lta(d_from=d_from, d_to=d_to)
        )

    def query_validations(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        df = parse_base_output(
            super().query_validations(d_from=d_from, d_to=d_to)
        ).rename(columns=to_snake_case).drop(columns=['last_modified_on'])
        #df['last_modified_on'] = pd.to_datetime(df['last_modified_on'], utc=True).dt.tz_convert('europe/amsterdam')

        return df

    def query_status(self, d_from: pd.Timestamp, d_to: pd.Timestamp) -> pd.DataFrame:
        return parse_base_output(
            super().query_status(d_from=d_from, d_to=d_to)
        ).drop(columns=['lastModifiedOn'])