from qapio_python_core import query
from dataclasses import dataclass, make_dataclass
from typing import Generic, TypeVar, Callable, TypedDict, Any
from abc import ABC, abstractmethod

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class Query(Generic[TRequest, TResponse]):
    @abstractmethod
    def invoke(self, request: TRequest) -> TResponse:
        pass


@dataclass
class Arguments:
    from_date: str
    to_date: str


@dataclass
class Response:
    frolkm_date: str
    to_daste: int


class MyQuery(Query[Arguments, Response]):

    def invoke(self, request: int) -> float:
        return 12
        pass


@query
def calculate(args: Arguments) -> Response:

    print("AEKKD")

    return Response(args.from_date, args.to_date)
