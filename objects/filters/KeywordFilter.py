from typing import Literal
from objects.filters.Filter import Filter


class KeywordFilter(Filter):
    keywords: list[str]
