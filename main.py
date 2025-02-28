import json
from typing import Annotated, Optional
from fastapi import FastAPI, Form, Request
from env import setup_secrets
from helpers import create_task
from indexer.index import index
from middleware import VerifyKeyMiddleware
from create import createKey
from celery import Celery
import os

from objects.Config import Config
from objects.PDFFile import PDFFile
from objects.PageRouter import PageRouterParameters
from fastapi import FastAPI, File, UploadFile
import tempfile
import uuid

from objects.filters.ContentTypeFilter import ContentTypeFilter
from objects.filters.CustomFilter import CustomFilter
from objects.filters.KeywordFilter import KeywordFilter
from objects.filters.PageNumberFilter import PageNumberFilter
from objects.filters.PageOrientationFilter import PageOrientationFilter
from structs import ExtractForm

app = Celery("main", broker="redis://localhost")


try:
    setup_secrets()
except:
    pass


@app.task
def indexer(url: str, filters: list[any]):
    index(url, filters)


api = FastAPI()

api.add_middleware(VerifyKeyMiddleware)


@api.post("/api/extract")
def accept_file_and_extract(request: Request, form: ExtractForm):
    uid = create_task(request.state.key_id)
    indexer.delay(form.url, [t.model_dump() | {
                  "type": (str(t.__class__.__name__))} for t in form.filters])
    return {"file_id": uid}


@api.post("/api/file")
def accept_file_and_index(file: Annotated[bytes, File()], webhook_url: Annotated[str, Form()], config: Annotated[str, Form()]):
    file_id = uuid.uuid4()
    config_json = json.loads(config)
    config_obj = Config(**config_json)
    indexer.delay(file, webhook_url, config_obj.page_router_parameters)
    return {"file_id": file_id}


@api.get("/ping")
def ping_pong():
    return "pong"
