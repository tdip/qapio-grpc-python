from qapio_python_core.qapi.Qapi import TimeSeriesApi, SqlApi
from typing import List, Union, TypedDict
from pandas import Timestamp, DataFrame, Series, Timedelta, offsets, MultiIndex, to_datetime, read_csv, melt


class Logger:
    def __init__(self, endpoint):
        self.__input = endpoint

    def info(self, message: str):
        self.__input.on_next({"value": message})


class Context:
    def __init__(self, qapi, dates, members, universe_name, logger: Logger):
        self.qapi = qapi
        self.dates = dates
        self.members = members
        self.universe_name = universe_name
        self.__logger = logger

    def time_series(self, node_id: str) -> TimeSeriesApi:
        return self.qapi.time_series(node_id)


    def endpoint(self, node_id: str):
        return self.qapi.endpoint(node_id)

    def time_series(self, node_id: str, bucket: str, measurements: List[str], fields: List[str], from_date: Union[Timestamp, str],
                    to_date: Union[Timestamp, str], tags: dict = dict({})):
        return self.qapi.time_series(node_id, bucket, measurements, fields, from_date, to_date)

    def sql(self, node_id: str) -> SqlApi:
        return self.qapi.sql(node_id)

    def source(self, expression: str):
        return self.qapi.source(expression)

    def query(self, expression: str):
        return self.qapi.query(expression)

    def logger(self):
        return self.__logger
