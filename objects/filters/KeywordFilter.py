from typing import Literal

from pydantic import BaseModel
from objects.filters.Filter import Filter


class KeywordFilter(Filter, BaseModel):
    keywords: list[str]
