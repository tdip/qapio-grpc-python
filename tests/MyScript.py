from qapio_python_core.screening import factor, Context, FactorResult

@factor
class MyFactor:
    def __init__(self):
        pass

    def begin(self, context: Context):
        pass

    def formula(self, result: FactorResult, context: Context):
        context.time_series("MyInfluxNode").dataset("EXTRACT", ["EM"], ["VOLATILITY"], "2000-01-01", "2023-03-01")
        result.value = 50.655





































































































