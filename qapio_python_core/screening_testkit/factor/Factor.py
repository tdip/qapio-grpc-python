import traceback
from pandas import Timestamp
from pykka import ThreadingActor
import os
from qapio_python_core import Qapi
from qapio_python_core.screening import FactorResult
from qapio_python_core.screening.shared.Context import Context


class Factor:
    def __init__(self, endpoint, instance, request):
        super().__init__()
        self.__api = Qapi(endpoint, sync=True)
        self.__instance = instance
        self.on_receive(request)

    def get_dates(self, data):
        parsed = {}

        keys = list(data.keys())
        keys.sort()

        for d in keys:
            parsed[Timestamp(d, tz='utc')] = data[d]

        return parsed
    def on_receive(self, request):
        message = request["universes"]
        node_id = request["universeId"]
        try:
            results = {}
            dates = self.get_dates(message)

            context = Context(self.__api)

            self.__instance.begin(context)

            for date, universe in dates.items():
                results[date.strftime("%Y-%m-%dT%H:%M:%SZ")] = []
                for member in universe:
                    factor_date_result = FactorResult(node_id, member["measurement"], date, request["nodeId"])
                    self.__instance.formula(factor_date_result, context)
                    if factor_date_result.value is not None:
                        for r in factor_date_result.results():
                            results[r["time"]].append(r)

            print({"results": results})
        except Exception as ex:
            traceback.print_exc()
            # traceback = ex.__traceback__
            #
            # while traceback:
            #     print_to_stderr("{}: {}".format(traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))
            #     traceback = traceback.tb_next

def factor():
    def decorator(cls):
        class DecoratedClass(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def run(self):
                if hasattr(self, "wrapper"):
                    print("Running MyClass with arg={} and test_arg={}".format(1, 2))
                else:
                    print("Running MyClass with arg={}".format(5))

        mode = os.environ.get("MODE")

        if mode != "PROD":
            instance = DecoratedClass()

            if hasattr(instance, "test_cases"):
                for case in instance.test_cases:
                    print(case)
        else:
            instance = DecoratedClass()
            print("TO!")
        #instance.run()


        return DecoratedClass

    return decorator


def test_data(endpoint, factor_id, universe_id, universes):
    def decorator(cls):
        class DecoratedClass(cls):
            def __init__(self, *args, **kwargs):
                mode = os.environ.get("MODE")
                if mode != "PROD":
                    if hasattr(self, "test_cases"):
                        self.test_cases = self.test_cases + [Factor(endpoint, self, {"nodeId": factor_id, "universeId": universe_id, "universes": universes})]
                    else:
                        self.test_cases = [Factor(endpoint, self, {"nodeId": factor_id, "universeId": universe_id, "universes": universes})]
                super().__init__(*args, **kwargs)

        return DecoratedClass

    return decorator


