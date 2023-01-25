from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from typing import List, Union, TypedDict

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

    def mutation(self, node_id: str, command: str, arguments: List[Union[str, int, float, bool]] = [], options: Options = {}):
        return self.__client.execute(self.__mutation, variable_values={"nodeId": node_id, "command": [command]+arguments})
