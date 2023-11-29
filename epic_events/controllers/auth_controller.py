from functools import wraps
from json import dump, load
from json.decoder import JSONDecodeError
from os import getenv

import click
from jwt import encode, decode, InvalidTokenError
from sqlalchemy import select

from epic_events.models import User
from epic_events.views.base import display_not_connected_error, display_invalid_token, \
    display_successful_connection, display_auth_data_entry_error, display_auth_already_connected

JWT_KEY = "secret"
TOKEN_FILE_PATH = "config.json"


@click.group()
@click.pass_context
def auth(ctx):
    ctx.ensure_object(dict)


def verify_token(token):
    return decode(token, JWT_KEY, algorithms=["HS256"])


def get_token():
    try:
        with open(TOKEN_FILE_PATH, 'r') as f:
            data = load(f)
            return data.get('token', None)
    except (JSONDecodeError, FileNotFoundError):
        return None


def check_auth(function):
    @wraps(function)
    def wrapper(ctx, *args, **kwargs):
        session = ctx.obj["session"]
        token = get_token()
        if not token:
            return display_not_connected_error()
        try:
            auth_id = verify_token(token)
            current_user = session.scalar(select(User).where(User.id == auth_id["id"]))
            # Verify that the user exists
            if not current_user:
                return display_invalid_token()
            ctx.obj["current_user"] = current_user
            return function(ctx, *args, ** kwargs)
        except InvalidTokenError:
            return display_invalid_token()
    return wrapper


@auth.command()
@click.option("-e", "--email", required=True, type=str, prompt="Enter your email")
@click.password_option(prompt="Enter your password")
@click.pass_context
def login(ctx, email, password):
    """
    Log in the user with the provided email and password.

    Args:
        ctx (click.Context): The Click context object.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The result of the login operation.
    """
    session = ctx.obj["session"]
    user = session.scalar(select(User).where(User.email == email))
    if not (user and user.check_password(password)):
        return display_auth_data_entry_error()
    if get_token():
        return display_auth_already_connected()
    token = encode({"id": user.id}, JWT_KEY, algorithm="HS256")
    with open(TOKEN_FILE_PATH, "w") as f:
        dump({"token": token}, f)
    return display_successful_connection(login=True)


@auth.command()
@click.confirmation_option(prompt="Are you sure you want to logout?")
def logout():
    try:
        with open(TOKEN_FILE_PATH, "r") as f:
            data = load(f)
            del data["token"]
        with open(TOKEN_FILE_PATH, "w") as f:
            dump(data, f)
        return display_successful_connection(login=False)
    except FileNotFoundError:
        return display_not_connected_error()


if __name__ == "__main__":
    auth()

