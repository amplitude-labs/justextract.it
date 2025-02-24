from typing import Literal
from commons.chunk import chunk
from nodes.Node import Node


class Table(Node):
    node: Literal["table"]
    rows: list[dict[str, str]]
