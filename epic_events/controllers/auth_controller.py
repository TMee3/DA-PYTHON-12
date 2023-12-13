import json
import os
from functools import wraps

import click
from jwt import InvalidTokenError, decode, encode
from sqlalchemy import select

from epic_events.models import User
from epic_events.views.auth_view import (display_auth_already_connected,
                                         display_auth_data_entry_error,
                                         display_invalid_token,
                                         display_not_connected_error,
                                         display_successful_connection)

TOKEN_FILE_PATH = "auth_token.json"
ERROR_MESSAGES = {
    "json_decode_error": "JSON decode error",
    "token_error_invalid": "Invalid token error",
    "logout_confirmation": "Are you sure you want to logout?",
}


def get_jwt_key():
    return os.getenv("JWT_KEY")


def verify_token(token):
    return decode(token, get_jwt_key(), algorithms=["HS256"])


def get_token():
    try:
        with open(TOKEN_FILE_PATH, "r") as f:
            data = json.load(f)
            return data.get("token", None)
    except json.JSONDecodeError as e:
        return None
    except FileNotFoundError:
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
            ctx.obj["current_user"] = current_user
            return function(ctx, *args, **kwargs)
        except InvalidTokenError as e:
            return display_invalid_token()

    return wrapper


@click.group()
@click.pass_context
def auth(ctx):
    ctx.ensure_object(dict)


@auth.command()
@click.option("-e", "--email", required=True, type=str)
@click.password_option()
@click.pass_context
def login(ctx, email, password):
    session = ctx.obj["session"]
    user = session.scalar(select(User).where(User.email == email))

    if not (user and user.check_password(password)):
        return display_auth_data_entry_error()
    if get_token():
        return display_auth_already_connected()

    token = encode({"id": user.id}, get_jwt_key(), algorithm="HS256")
    with open(TOKEN_FILE_PATH, "w") as f:
        json.dump({"token": token}, f)
    return display_successful_connection(login=True)


@auth.command()
@click.confirmation_option(prompt=ERROR_MESSAGES["logout_confirmation"])
def logout():
    with open(TOKEN_FILE_PATH, "r") as f:
        data = json.load(f)
        del data["token"]
    with open(TOKEN_FILE_PATH, "w") as f:
        json.dump(data, f)
    return display_successful_connection(login=False)
