import requests
import reactivex

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


client = QapiHttpClient("https://127.0.0.1:5035")

print(client.query("Sql.TimeSeries({bucket: 'prices', measurements: ['XQG0NZ-R'],  fields: ['p_price'], fromDate: '2001-01-01', toDate: '2024-01-01'})").json())

client.source("Source.Tick(100).Take(100)").subscribe(on_next=lambda x: print(x))
