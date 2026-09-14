from argparse import _SubParsersAction

from app.cli_handlers import user_cli_handler as handler

# Main Functions

def setup_user_parser(subparsers: _SubParsersAction) -> None:
  user_parser = subparsers.add_parser("user", help="Operations on user")
  user_subparser = user_parser.add_subparsers(dest="action", required=True, help="Action")

  _register_user_parser(user_subparser)


# Helper Functions

def _register_user_parser(subparsers: _SubParsersAction) -> None:
  register_parser = subparsers.add_parser("register", help="Register user")

  register_parser.add_argument(
    "-u",
    "--username",
    required=True,
    type=str,
    help="Enter username to create account"
  )

  register_parser.add_argument(
    "-e",
    "--email",
    required=True,
    type=str,
    help="Enter email to create account"
  )

  register_parser.add_argument(
    "-p",
    "--password",
    required=True,
    type=str,
    help="Enter password to create account"
  )

  register_parser.set_defaults(func=handler.user_register_handler)