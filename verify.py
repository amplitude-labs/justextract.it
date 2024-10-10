import requests
import os
from dotenv import load_dotenv

load_dotenv()

UNKEY_API_ID = os.getenv("UNKEY_API_ID")
UNKEY_ROOT_KEY = os.getenv("UNKEY_ROOT_KEY")

def verifyKey(key):
    url = "https://api.unkey.dev/v1/keys.verifyKey"

    payload = {
        "apiId": UNKEY_API_ID,
        "key": key
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()