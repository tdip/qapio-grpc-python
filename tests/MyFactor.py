from tests.MyScript import factor, Context, FactorResult


@factor
class MyFactor:
    def __init__(self):
        pass

    def begin(self, context: Context):
        pass

    def formula(self, result: FactorResult, context: Context):
        result.value = 124







