from typing import Optional
from pydantic import BaseModel

from objects.PageRouter import PageRouterParameters


class Config(BaseModel):
    page_router_parameters: Optional[PageRouterParameters] = None
