import requests
import reactivex
from io import StringIO
import json
from pandas import read_json, DataFrame
class QapiHttpClient:
    def __init__(self, url: str):
        self.__url = url

    def query(self, expression: str):
        return requests.get(f"{self.__url}/query/{expression}", verify=False)

    def source(self, expression: str):

        session = requests.Session()

        return reactivex.from_iterable(session.get(
            f"{self.__url}/source/{expression}",
            verify=False, stream=True
        ).iter_lines(decode_unicode=True))


client = QapiHttpClient("https://127.0.0.1:5032")


client.source(f"Source.Tick(1000)").subscribe(on_next=lambda x: print(x))
