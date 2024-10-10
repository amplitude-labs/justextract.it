import requests
import os
from dotenv import load_dotenv

load_dotenv()

UNKEY_API_ID = os.getenv("UNKEY_API_ID")
UNKEY_ROOT_KEY = os.getenv("UNKEY_ROOT_KEY")

def createKey():
    url = "https://api.unkey.dev/v1/keys.createKey"

    payload = {
        "apiId": UNKEY_API_ID,
        "prefix": "fast_api",
        "name": "FastAPI",
        "meta": {"randomNumber": 13213131141},
        "remaining": 3
    }

    headers = {
        "Authorization": f"Bearer {UNKEY_ROOT_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()
