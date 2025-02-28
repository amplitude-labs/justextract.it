import requests
import os
from dotenv import load_dotenv


def createKey():
    UNKEY_API_ID = os.getenv("UNKEY_API_ID")
    UNKEY_ROOT_KEY = os.getenv("UNKEY_ROOT_KEY")

    url = "https://api.unkey.dev/v1/keys.createKey"
    payload = {
        "apiId": UNKEY_API_ID,
        "prefix": "fast_api",
        "name": "FastAPI",
        "meta": {"randomNumber": 13213131141},
        "remaining": 300
    }

    headers = {
        "Authorization": f"Bearer {UNKEY_ROOT_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()
