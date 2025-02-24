import json
import tempfile
from typing import Annotated, Optional

from fastapi import File
import requests
from objects.PDFFile import PDFFile
from objects.PageRouter import PageRouterParameters


def index(file: Annotated[bytes, File()], webhook_url: str, page_router_paramters: Optional[PageRouterParameters] = None):
    with tempfile.NamedTemporaryFile("wb") as f:
        f.write(file)
        pdf_file = PDFFile(f.name)
        nodes = pdf_file.get_nodes(page_router_params=page_router_paramters)
        requests.post(webhook_url, json={
                      "nodes": [node.__dict__ for node in nodes]})
