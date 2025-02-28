from pydantic import BaseModel
from objects.filters.Filter import Filter


class PageNumberFilter(Filter, BaseModel):
    pages: list[int]
