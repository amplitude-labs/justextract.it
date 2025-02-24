from typing import Literal
from objects.filters.Filter import Filter


class PageOrientationFilter(Filter):
    orientation: Literal["portrait", "landscape"]
