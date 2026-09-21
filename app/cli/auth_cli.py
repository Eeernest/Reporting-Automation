from argparse import _SubParsersAction

from app.cli_handlers import auth_cli_handler as handler

# Main Functions

def setup_auth_parser(subparsers: _SubParsersAction) -> None:
  auth_parser = subparsers.add_parser("auth", help="Operations on auth")
  auth_subparser = auth_parser.add_subparsers(
    dest="action",
    required=True,
    help="Auth action"
  )

  _login_parser(auth_subparser)


# Helper Functions

def _login_parser(subparsers: _SubParsersAction) -> None:
  login_parser = subparsers.add_parser("login", help="Login to api (username and password needed)")

  login_parser.add_argument(
    "-u",
    "--username",
    required=True,
    type=str,
    help="Enter username to login"
  )

  login_parser.add_argument(
    "-p",
    "--password",
    required=True,
    type=str,
    help="Enter password to login"
  )

  login_parser.set_defaults(func=handler.auth_login_handler)