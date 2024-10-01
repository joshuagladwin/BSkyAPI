import json
from atproto_client import Client


def bsky_login():
    with open("credentials.json", "r") as f:
        credentials = json.load(f)

    username = credentials["username"]
    password = credentials["password"]

    client = Client()
    client.login(username, password)

    return client
