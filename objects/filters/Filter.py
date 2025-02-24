from pydantic import BaseModel


class Filter(BaseModel):
    include: bool = False
