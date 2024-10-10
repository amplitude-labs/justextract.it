from fastapi import FastAPI
from middleware import VerifyKeyMiddleware
from create import createKey

app = FastAPI()

app.add_middleware(VerifyKeyMiddleware)

@app.get("/api/hello")
def hello():
    return "Hello World!"

@app.get("/api/create")
def create_key():
    return createKey()

@app.post("/api/protected")
def verify_key():
    return {"message": "Protected route accessed"}
