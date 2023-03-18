import traceback

from pandas import Timestamp
from pykka import ThreadingActor

from qapio_python_core import load_qapio_manifest
from qapio_python_core.qapi.client.Client import QapioGrpc
from qapio_python_core.screening.shared.Context import Context
import json
import hashlib

class UniverseResult:
    def __init__(self, measurement: str, date: Timestamp):
        self.measurement = measurement
        self.date = date
        self.value = []

    def results(self):
        return self.value

class Universe(ThreadingActor):
    def __init__(self, api, instance):
        super().__init__()
        self.__api = api
        self.__log = api.api
        self.__instance = instance()
        self.__input = api.input("RESPONSE").get()
        api.output("REQUEST", self.actor_ref)

    def get_dates(self, data):
        parsed = []

        data.sort()

        for d in data:
            parsed.append(Timestamp(d, tz='utc'))

        return parsed
    def on_receive(self, request):
        message = request["dates"]

        try:
            results = dict({'map': dict({}), 'index': dict({})})

            dates = self.get_dates(message)

            context = Context(self.__api.qapi, list(dates), [])

            self.__instance.begin(context)

            for date in dates:

                universe_result = UniverseResult(request["nodeId"], date)

                self.__instance.formula(universe_result, context)

                raw = universe_result.results()

                json_representation = json.dumps(raw)
                key = hashlib.md5(json_representation.encode()).hexdigest()

                if key not in results.get("index"):
                    results.get("index")[key] = raw

                #out_data[date] = uni

                #out_data.get("universeMap")[date] = key
                results.get("map")[date.strftime("%Y-%m-%dT%H:%M:%SZ")] = key


            #                results[date.strftime("%Y-%m-%dT%H:%M:%SZ")] = universe_result.results()

            self.__input.proxy().on_next(results)
        except Exception as ex:
            traceback.print_exc()
            # traceback = ex.__traceback__
            #
            # while traceback:
            #     print_to_stderr("{}: {}".format(traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))
            #     traceback = traceback.tb_next





def universe(fn):
    manifest = load_qapio_manifest()
    qapio = QapioGrpc('localhost:5113', "http://localhost:4000/graphql", manifest)
    Universe.start(qapio, fn)
