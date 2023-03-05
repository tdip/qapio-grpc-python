from qapio_python_core.qapi.Qapi import TimeSeriesApi
class Context:
    def __init__(self, qapi):
        self.qapi = qapi

    def time_series(self, node_id: str) -> TimeSeriesApi:
        return self.qapi.time_series(node_id)

