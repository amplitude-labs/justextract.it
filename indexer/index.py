import json
import tempfile
from typing import Annotated, Optional

from fastapi import File
import requests
from helpers import update_status
from objects.PDFFile import PDFFile
from objects.PageRouter import PageRouterParameters
from structs import ExtractForm


from objects.filters.ContentTypeFilter import ContentTypeFilter
from objects.filters.CustomFilter import CustomFilter
from objects.filters.KeywordFilter import KeywordFilter
from objects.filters.PageNumberFilter import PageNumberFilter
from objects.filters.PageOrientationFilter import PageOrientationFilter


def index(id: str, url: str, filters: list[any]):
    with tempfile.NamedTemporaryFile("wb") as f:
        data = requests.get(url).content
        f.write(data)
        f.flush()
        pdf_file = PDFFile(f.name)
        for index, filter in enumerate(filters):
            fil = pdf_file.filter_names[filter["type"]](**filter)
            pdf_file.filter_mappings[type(fil)](fil)
            update_status(id, index / (len(filters) + 1),
                          filter["type"] + " done.")
        nodes = pdf_file.get_nodes()
        update_status(id, index / (len(filters) + 1),
                      filter["type"] + " done.")
        print(nodes)
