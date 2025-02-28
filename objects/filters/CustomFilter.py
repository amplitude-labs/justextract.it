from typing import Literal

from pydantic import BaseModel
from objects.filters.Filter import Filter


class CustomFilter(Filter, BaseModel):
    query: str
