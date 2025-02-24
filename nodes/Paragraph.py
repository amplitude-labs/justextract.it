from typing import Literal
from commons.chunk import chunk
from nodes.Node import Node


class Paragraph(Node):
    node: Literal["text"]
    chunks: list[str]
