from typing import Literal
from objects.filters.Filter import Filter


class ContentTypeFilter(Filter):
    content_types: list[Literal["table", "image", "text", "hyperlink"]]
