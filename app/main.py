import argparse

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.cli.auth_cli import setup_auth_parser
from app.cli.user_cli import setup_user_parser
from app.core.config import settings
from app.core.exceptions import AppError
from app.core.exception_handler import custom_exc_handler, validation_exc_handler
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router

# API

app = FastAPI()


# Exception Handler

app.add_exception_handler(AppError, custom_exc_handler)
app.add_exception_handler(RequestValidationError, validation_exc_handler)


# Router

app.include_router(auth_router)
app.include_router(user_router)


# CLI

def parser():
  parser = argparse.ArgumentParser(description="Main CLI for API")

  parser.add_argument(
    "--api-url",
    default=settings.APP_URL,
    help="API URL Address"
  )

  resource_subparser = parser.add_subparsers(
    dest="resource",
    required=True,
    help="Resources"
  )

  setup_auth_parser(resource_subparser)
  setup_user_parser(resource_subparser)

  args = parser.parse_args()

  if hasattr(args, "func"):
    args.func(args)

  else:
    parser.print_help()

if __name__ == "__main__":
  parser()