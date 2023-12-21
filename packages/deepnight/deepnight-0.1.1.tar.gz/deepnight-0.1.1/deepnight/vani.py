import requests
import os

def vani(file_path: str, model="vani-v1"):
    resp = requests.post("https://api.deepnight.tech/v1", data={
        "file": open(file_path, "rb"),
        "model": model
    })

    return resp.json()