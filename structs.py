
from pydantic import BaseModel
from objects.filters.ContentTypeFilter import ContentTypeFilter
from objects.filters.CustomFilter import CustomFilter
from objects.filters.KeywordFilter import KeywordFilter
from objects.filters.PageNumberFilter import PageNumberFilter
from objects.filters.PageOrientationFilter import PageOrientationFilter


class ExtractForm(BaseModel):
    url: str
    filters: list[ContentTypeFilter | CustomFilter |
                  KeywordFilter | PageNumberFilter | PageOrientationFilter]
