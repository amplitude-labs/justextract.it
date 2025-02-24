import requests
import os
from dotenv import load_dotenv

load_dotenv()


def verifyKey(key):
    url = "https://api.unkey.dev/v1/keys.verifyKey"

    UNKEY_API_ID = os.getenv("UNKEY_API_ID")
    UNKEY_ROOT_KEY = os.getenv("UNKEY_ROOT_KEY")

    payload = {
        "apiId": UNKEY_API_ID,
        "key": key
    }

    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.json())
    return response.json()
