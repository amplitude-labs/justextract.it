from typing import Literal
from commons.chunk import chunk
from nodes.Node import Node


class Image(Node):
    node: Literal["image"]
    chunks: list[str]
