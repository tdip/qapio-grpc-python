from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from typing import List, Union, TypedDict
import json
from influxdb_client.client.flux_csv_parser import FluxCsvParser, FluxSerializationMode
from io import StringIO
from pandas import DataFrame
import csv as csv_parser


class Options(TypedDict):
    key: str
    value: Union[str, int, float, bool]


class Qapi:
    def __init__(self, http_endpoint: str, ws_endpoint: str = ""):
        self.__http_endpoint = http_endpoint
        self.__ws_endpoint = ws_endpoint
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

    def query(self, node_id: str, command: str, arguments: List[Union[str, int, float, bool]] = [], options: Options = {}):
        result = self.__client.execute(self.__query, variable_values={"nodeId": node_id, "command": [command]+arguments})
        return result

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


class TimeSeriesApi:
    def __init__(self, client: Qapi, node_id: str):
        self.__client = client
        self.__node_id = node_id

    def dataset(self, bucket: str, measurements: List[str], fields: List[str], from_date, to_date, tags: dict = dict({})):
        data = self.__client.query(self.__node_id, "time-series", [",".join(measurements), ",".join(fields), from_date, to_date, bucket])
        csv = json.loads(data["cmd"]["payload"]["json"])
        df = QapioFluxCsvParser.parse_to_dataframe({"value": csv})

        return df
