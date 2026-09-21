from argparse import Namespace
import json
from pathlib import Path
import requests

from app.core.config import settings

APP_URL = settings.APP_URL

# Main Functions

def auth_login_handler(args: Namespace) -> None:
  endpoint_url = f"{APP_URL}/login"

  payload = {
    "username": args.username,
    "password": args.password
  }

  try:
    response = requests.post(endpoint_url, data=payload)
    response.raise_for_status()

    token_data = response.json()

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    token_type = token_data.get("token_type")

    _save_tokens(
      access_token,
      refresh_token,
      token_type
    )

    print("User successfully logged in")

  except requests.exceptions.HTTPError as err:
    print(f"HTTP Error: {err}")

    if response.content:
      print(f"Detail: {response.text}")


# Helper Functions

def _save_tokens(
    access_token: str,
    refresh_token: str,
    token_type: str
) -> None:
  if not access_token or not refresh_token or not token_type:
    print("API did not return complete token data")
    return
  
  payload = {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": token_type
  }

  token_file = Path.home() / settings.TOKEN_STORAGE_PATH
  token_file.write_text(json.dumps(payload))