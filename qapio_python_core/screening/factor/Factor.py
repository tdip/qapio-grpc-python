from pandas import Timestamp
from pykka import ThreadingActor
from qapio_python_core import load_qapio_manifest
from qapio_python_core.qapi.client.Client import QapioGrpc

class FactorResult:
    def __init__(self, measurement: str, date: Timestamp, field: str):
        self.measurement = measurement
        self.date = date
        self.field = field
        self.value = None

    def results(self):
        return [{"measurement": self.measurement, "time": self.date.strftime("%Y-%m-%dT%H:%M:%SZ"), "fields": {self.field: self.value}, "tags": {}}]

class Context:
    def __init__(self, qapi):
        self.qapi = qapi

    def time_series(self, node_id: str):
        return self.qapi.time_series(node_id)


class Factor(ThreadingActor):
    def __init__(self, api, instance):
        super().__init__()
        self.__api = api
        self.__log = api.api
        self.__instance = instance()
        self.__input = api.input("RESPONSE").get()
        api.output("REQUEST", self.actor_ref)

    def get_dates(self, data):
        parsed = {}

        keys = list(data.keys())
        keys.sort()

        for d in keys:
            parsed[Timestamp(d, tz='utc')] = data[d]

        return parsed
    def on_receive(self, request):
        message = request["universes"]

        try:
            results = {}
            dates = self.get_dates(message)
            context = Context(self.__api.qapi)
            self.__instance.begin(context)
            for date, universe in dates.items():
                results[date.strftime("%Y-%m-%dT%H:%M:%SZ")] = []
                for member in universe:
                    factor_date_result = FactorResult(member["measurement"], date, request["nodeId"])
                    self.__instance.formula(factor_date_result, context)
                    for r in factor_date_result.results():
                        results[r["time"]].append(r)

            self.__input.proxy().on_next({"results": results})
        except Exception as ex:

            traceback = ex.__traceback__

            while traceback:
                print_to_stderr("{}: {}".format(traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))
                traceback = traceback.tb_next





def factor(fn):
    manifest = load_qapio_manifest()
    qapio = QapioGrpc('localhost:5113', "http://localhost:4000/graphql", manifest)
    Factor.start(qapio, fn)



