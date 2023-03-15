from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import RequestsHTTPTransport
from typing import List, Union, TypedDict
import json
from influxdb_client.client.flux_csv_parser import FluxCsvParser, FluxSerializationMode
from io import StringIO
from pandas import DataFrame
import csv as csv_parser
from numpy import finfo, float32, nan
from pandas.api.types import is_numeric_dtype
from pandas import Timestamp, DataFrame, Series, Timedelta, offsets, MultiIndex, to_datetime
import sys
from typing import Union

class Options(TypedDict):
    key: str
    value: Union[str, int, float, bool]


class Qapi:
    def __init__(self, http_endpoint: str, ws_endpoint: str = "", sync: bool = False):
        self.__cache = {}
        self.__time_series = {}
        self.__http_endpoint = http_endpoint
        self.__ws_endpoint = ws_endpoint
        if sync:
            self.http_transport = RequestsHTTPTransport(url=http_endpoint)
        else:
            self.http_transport = AIOHTTPTransport(url=http_endpoint)

        self.__client = Client(transport=self.http_transport, fetch_schema_from_transport=True)
        self.__query = gql(
            """
            query Command($nodeId: String!, $command: [String!]!) {
                cmd(nodeId: $nodeId, command: $command) {
                    payload {typeName, json}
                    type,
                    meta {correlationId}
                }
            }
        """
        )
        self.__mutation = gql(
            """
            mutation Command($nodeId: String!, $command: [String!]!) {
                cmd(nodeId: $nodeId, command: $command) {
                    requestId,
                    error
                }
            }
        """
        )

    def time_series(self, node_id):
        if node_id in self.__time_series:
            return self.__time_series[node_id]
        ts = TimeSeriesApi(self, node_id)
        self.__time_series[node_id] = ts
        return ts

    def query(self, node_id: str, command: str, arguments: List[Union[str, int, float, bool]] = [], options: Options = {}):
        cache_key = json.dumps({"nodeId": node_id, "command": [command]+arguments})
        if cache_key in self.__cache:
            return self.__cache[cache_key]
        result = self.__client.execute(self.__query, variable_values={"nodeId": node_id, "command": [command]+arguments})
        self.__cache[cache_key] = result
        return result["cmd"]["payload"]["json"]

    def mutate(self, node_id: str, command: str, arguments: List[Union[str, int, float, bool]] = [], options: Options = {}):
        return self.__client.execute(self.__mutation, variable_values={"nodeId": node_id, "command": [command]+arguments})


class QapioFluxCsvParser(FluxCsvParser):

    def __init__(
        self,
        data: str,
        serialization_mode: FluxSerializationMode,
        data_frame_index: List[str] = None):

        FluxCsvParser.__init__(self, None, serialization_mode, data_frame_index)
        self.__data = data

    def __enter__(self):
        a = StringIO(self.__data)
        #a = self.__data.splitlines()
        self._reader = csv_parser.reader(
            a

        )
        return self

    def __exit__(self, *args, **kwargs):
        pass

    @staticmethod
    def parse_to_dataframe(data: dict) -> DataFrame:
        if data["value"] == "":
            return None
        parser = QapioFluxCsvParser(data["value"], FluxSerializationMode.dataFrame)
        values = list(parser.generator())
        #rint(values)
        if len(values) == 1:

            return values[0]
        else:
            return None


def timestamp2str(date: Timestamp):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')

class DataSet:
    def __init__(self, data_frame):

        self.__series = dict({})
        if data_frame is None:
            return

        if data_frame.empty:
            return
        nonCatCols = ["_time", "_value"]

        for col in data_frame.columns:
            if col not in nonCatCols:
                data_frame[col] = data_frame[col].astype("category")

        #print(data_frame.dtypes)
        # data_frame["_time"] = data_frame["_time"].map(lambda x: x.tz_convert('UTC'))

        try:
            response = data_frame.set_index(MultiIndex.from_frame(data_frame[[
                "_measurement", "_field", "_time",
            ]   ], names=["_measurement", "_field", "_time", ]))


            #response = response.tz_localize('UTC', level=1)

            response = response.sort_index()
            a = finfo(float32).min
            response = response.replace(to_replace=a,
                                        value=nan)
            self.__data_frame = response

        except Exception as e:
            print(e)


    @property
    def data_frame(self):
        return self.__data_frame

    def series(self, measurement: str, field: str,
               from_date: Timestamp =
               None, to_date: Timestamp = None) -> Series:


        try:
            # series = self.__data_frame[
            #     (self.__data_frame._measurement == measurement) & (self.__data_frame._field == field)]

            if measurement+field not in self.__series:

                colNames = list(self.__data_frame)

                if field in colNames:
                    data = self.__data_frame.loc[measurement, :, : ]
                    series = Series(data=data[field].values, index=data["_time"].values)
                    series = series.tz_localize('UTC', level=0)
                    self.__series[measurement+field] = series
                else:
                    data = self.__data_frame.loc[measurement, field, : ]

                    series = Series(data=data["_value"].values, index=data["_time"].values)
                    series = series.tz_localize('UTC', level=0)
                    self.__series[measurement+field] = series

            series = self.__series.get(measurement+field)

            #series = Series(data=series["_value"].values, index=series["_time"].values)
            #series = series.tz_localize('UTC', level=0)

            if from_date is None and to_date is None:
                series = series

            if from_date is not None and to_date is not None:
                series = series.loc[from_date:to_date]

            if from_date is not None and to_date is None:
                series = series.loc[from_date:]

            if from_date is None and to_date is not None:
                series = series.loc[:to_date]

            if series is None:
                return None

            if len(series.index) == 0:
                return None

            if is_numeric_dtype(series):
                return series[series < 3.4e38]

            return series.dropna()
        except:
            return None


    def point_series(self, measurements: List[str], field: str,
                     date: Timestamp):

        data = []

        for ticker in measurements:
            p = self.point(
                ticker,
                field,
                date)

            if p is None:
                p = nan

            data.append(p)

        return Series(data, index=measurements)

    def point(self, measurement: str, field: str, date: Timestamp):
        series = self.series(measurement, field, date, date)

        if series is None:
            return None

        try:
            point = series[date]
            if isinstance(point, Series):
                print("Duplicate found.")
                print(measurement)
                print(field)
                return None
            return point
        except:
            return None

    def last(self, measurement: str, field: str, date: Timestamp):
        series = self.series(measurement, field, None, date)

        if series is None or len(series.tail(1).keys()) == 0:
            return None

        last = series.tail(1)[0]

        if isinstance(last, Series):
            print("Duplicate found.")
            print(measurement)
            print(field)
            return None

        return last



def transform_tags(tags):
    if not tags:
        return []
    kvps = []
    for key, values in tags.items():
        if not any('.' in value for value in values):
            kvp = ' or '.join(f'r.{key} == "{value}"' for value in values)
            kvps.append(kvp)
    return ['--Tag'] + ['\n' + kvp for kvp in kvps]

class TimeSeriesApi:
    def __init__(self, client: Qapi, node_id: str):
        self.__cache = {}

        self.__client = client
        self.__node_id = node_id

    def query(self, query):

        cache_key = json.dumps(query)

        if cache_key in self.__cache:
            return self.__cache[cache_key]

        data = self.__client.query(self.__node_id, "query", [query])
        csv = json.loads(data)
        df = QapioFluxCsvParser.parse_to_dataframe({"value": csv})
        self.__cache[cache_key] = df
        return df


    def dataset(self, bucket: str, measurements: List[str], fields: List[str], from_date: Union[Timestamp, str], to_date: Union[Timestamp, str], tags: dict = dict({})):

        if type(from_date) == Timestamp:
            from_date = timestamp2str(from_date)

        if type(to_date) == Timestamp:
            to_date = timestamp2str(to_date)

        cache_key = json.dumps([",".join(measurements), ",".join(fields), from_date, to_date, bucket] + transform_tags(tags))

        if cache_key in self.__cache:
            return self.__cache[cache_key]

        data = self.__client.query(self.__node_id, "time-series", [",".join(measurements), ",".join(fields), from_date, to_date, bucket] + transform_tags(tags))
        csv = json.loads(data)
        df = QapioFluxCsvParser.parse_to_dataframe({"value": csv})
        result = DataSet(df)
        self.__cache[cache_key] = result
        return result
