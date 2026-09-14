from argparse import Namespace
import requests

from app.core.config import settings

APP_URL = settings.APP_URL

# Main Functions

def user_register_handler(args: Namespace) -> None:
  endpoint_url = f"{APP_URL}/register_user"
  
  payload = {
    "username": args.username,
    "email": args.email,
    "password": args.password
  }

  try:
    response = requests.post(endpoint_url, json=payload)
    response.raise_for_status()

    print("User successfully registered")

  except requests.exceptions.HTTPError as err:
    print(f"HTTP Error: {err}")

    if response.content:
      print(f"Detail: {response.text}")