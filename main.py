import json
from typing import Annotated, Optional
from fastapi import FastAPI, Form
from env import setup_secrets
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

app = Celery("main", broker="redis://localhost")

try:
    setup_secrets()
except:
    pass


@app.task
def indexer(file: Annotated[bytes, File()], webhook_url: str, page_router_paramters: Optional[PageRouterParameters] = None):
    print(webhook_url)
    index(file, webhook_url, page_router_paramters)


api = FastAPI()

api.add_middleware(VerifyKeyMiddleware)


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
