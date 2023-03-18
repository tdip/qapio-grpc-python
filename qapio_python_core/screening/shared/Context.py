from qapio_python_core.qapi.Qapi import TimeSeriesApi
class Context:
    def __init__(self, qapi, dates, members, universe_name):
        self.qapi = qapi
        self.dates = dates
        self.members = members
        self.universe_name = universe_name

    def time_series(self, node_id: str) -> TimeSeriesApi:
        return self.qapi.time_series(node_id)

