import sys
import traceback
from pandas import Timestamp
from pykka import ThreadingActor
import os

from qapio_python_core import load_qapio_manifest
from qapio_python_core.qapi.client.Client import QapioGrpc
from qapio_python_core.screening.shared.Context import Context


def print_to_stderr(a):
    print(a, file=sys.stderr)


class FactorResult:
    def __init__(self, universe_id: str, measurement: str, date: Timestamp, field: str):
        self.__universe_id = universe_id
        self.measurement = measurement
        self.date = date
        self.field = field
        self.value = None

    def set_value(self, value):
        self.value = value

    def results(self):
        return [{"measurement": self.measurement, "time": self.date.strftime("%Y-%m-%dT%H:%M:%SZ"), "fields": {self.field: self.value}, "tags": {
            "FSYM_ID": self.__universe_id
        }}]


class Factor(ThreadingActor):
    def __init__(self, api, instance):
        super().__init__()
        self.__api = api
        self.__log = api.api
        self.__instance = instance
        self.__input = api.input("RESPONSE").get()
        self.__logger = api.input("LOG").get()
        api.output("REQUEST", self.actor_ref)

    def get_dates(self, data):
        parsed = {}

        keys = list(data.keys())
        keys.sort()

        for d in keys:
            parsed[Timestamp(d, tz='utc')] = data[d]

        return parsed
    def on_receive(self, request):
        message = request["universe"]
        universeId = request["measurement"]
        factor = request["factor"]
        try:
            results = {}
            dates = self.get_dates(message)

            all_members = []
            for date, value in message.items():
                all_members = all_members + [o.get("measurement") for o in value]

            context = Context(self.__api.qapi, list(dates.keys()), list(set(all_members)), universeId)

            self.__instance.begin(context)

            for date, universe in dates.items():
                results[date.strftime("%Y-%m-%dT%H:%M:%SZ")] = []
                for member in universe:
                    factor_date_result = FactorResult(universeId, member["measurement"], date, factor)
                    self.__instance.formula(factor_date_result, context)
                    if factor_date_result.value is not None:
                        for r in factor_date_result.results():
                            results[r["time"]].append(r)

            self.__input.proxy().on_next({"guid": request["guid"], 'data': results})
        except Exception as ex:
            self.__logger.proxy().on_next({"value": traceback.format_exc()})
            traceback.print_exc()


def factor(fn):


    instance = fn()

    if hasattr(instance, "test_cases"):
        print("Running in test mode.")

    else:
        manifest = load_qapio_manifest()
        gqlEndpoint = 'http://' + os.getenv('GQL_ENDPOINT') + ':4000/graphql'
        qapio = QapioGrpc(os.getenv('GRPC_ENDPOINT') + ':5113', 'https://' + os.getenv('GQL_ENDPOINT') + ':5035', manifest)
        Factor.start(qapio, instance)
