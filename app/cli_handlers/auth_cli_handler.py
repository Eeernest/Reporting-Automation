from argparse import Namespace
import json
from pathlib import Path
import requests

from app.core.config import settings

APP_URL = settings.APP_URL
token_file = Path.home() / settings.TOKEN_STORAGE_PATH

# Main Functions

def auth_login_handler(args: Namespace) -> None:
  endpoint_url = f"{APP_URL}/login"

  request_payload = {
    "username": args.username,
    "password": args.password
  }

  try:
    response = requests.post(endpoint_url, data=request_payload)
    response.raise_for_status()

    token_data = response.json()

    token_payload = {
      "access_token": token_data["access_token"],
      "refresh_token": token_data["refresh_token"],
      "token_type": token_data["token_type"]
    }

    _save_tokens(token_payload)

    print("User successfully logged in")

  except requests.exceptions.HTTPError as err:
    print(f"HTTP Error: {err}")

    if response.content:
      print(f"Detail: {response.text}")

def auth_logout_handler(args: Namespace) -> None:
  endpoint_url = f"{APP_URL}/logout"

  token_data = _load_tokens()

  if not token_data or not token_data["refresh_token"]:
    print("Refresh token error. Login again")
    return

  request_payload = {"refresh_token": token_data["refresh_token"]}

  try:
    response = requests.post(endpoint_url, json=request_payload)

    token_file.unlink()

    print("User successfully logged out")

  except requests.exceptions.HTTPError as err:
    print(f"HTTP Error: {err}")

    if response.content:
      print(f"Detail: {response.text}")


# Helper Functions

def _save_tokens(token_payload: dict) -> None:
  if not token_payload["access_token"] or not token_payload["refresh_token"] or not token_payload["token_type"]:
    print("API did not return complete token data")
    return

  token_file.write_text(json.dumps(token_payload))

def _load_tokens() -> dict | None:
  if not token_file.exists():
    return

  try:
    return json.loads(token_file.read_text())

  except json.JSONDecodeError:
    return