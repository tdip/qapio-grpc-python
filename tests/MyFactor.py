from qapio_python_core.screening_testkit import factor_test_case
from qapio_python_core.screening import Context, FactorResult, factor


@factor
@factor_test_case("http://localhost:4000/graphql", "MKT_CAP_LOCAL", "EM", {"2020-01-01": [{"measurement": "A", "meta": {}},{"measurement": "B", "meta": {}},{"measurement": "C", "meta": {}}]})
class MyFactor:
    def begin(self, context: Context):
        print("CALLED")

    def formula(self, result: FactorResult, context: Context):
        print("ELLE")
        result.value = 500



