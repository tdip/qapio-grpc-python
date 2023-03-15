from qapio_python_core.screening_testkit import test_data
from qapio_python_core.screening import Context, FactorResult, factor
from pandas import Timestamp
import os

# Set an environment variable

# Get the value of an environment variable


@factor()
@test_data("http://localhost:4000/graphql", "MKT_CAP_LOCAL", "EM", {"2020-01-01": [{"measurement": "A", "meta": {}}]})
@test_data("http://localhost:4000/graphql", "MKT_CAP_LOCAL", "EM", {"2020-01-01": [{"measurement": "A", "meta": {}}]})
@test_data("http://localhost:4000/graphql", "MKT_CAP_LOCAL", "EM", {"2020-01-01": [{"measurement": "A", "meta": {}}]})
class MyFactor:
    def begin(self, context: Context):
        print("CALLED")

    def formula(self, result: FactorResult, context: Context):
        print("ELLE")
        result.value = 500



