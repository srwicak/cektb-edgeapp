import hashlib
import json
from pathlib import Path

CREDENTIALS_PATH = Path("data/credentials.json")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def validate_local_password(password: str):
    if not CREDENTIALS_PATH.exists():
        raise Exception("No local credentials found")
    with open(CREDENTIALS_PATH, "r") as f:
        credentials = json.load(f)
    if hash_password(password) != credentials.get("password_hash"):
        raise Exception("Invalid local password")
    return True

def authenticate_server(username: str, password: str) -> str:
    # Simulasi autentikasi ke server
    if username == "test_user" and password == "test_password":
        return "server_token_example"
    return None
