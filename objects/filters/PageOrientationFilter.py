from typing import Literal

from pydantic import BaseModel
from objects.filters.Filter import Filter


class PageOrientationFilter(Filter, BaseModel):
    orientation: Literal["portrait", "landscape"]
