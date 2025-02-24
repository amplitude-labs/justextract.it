from typing import Literal
from objects.filters.Filter import Filter


class CustomFilter(Filter):
    query: str
