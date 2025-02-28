from typing import Literal

from pydantic import BaseModel
from objects.filters.Filter import Filter


class ContentTypeFilter(Filter, BaseModel):
    content_types: list[Literal["table", "image", "text", "hyperlink"]]
