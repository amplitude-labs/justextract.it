import inspect
from pydantic import BaseModel
import pydantic
from typing import Type, TypeVar

T = TypeVar("T")


class PageRouterParameters(BaseModel):
    limit: int
    query: str


def custom_func(T: T) -> T:
    return T(limit=9, query="")


a = custom_func(PageRouterParameters)


print(PageRouterParameters.schema_json())
