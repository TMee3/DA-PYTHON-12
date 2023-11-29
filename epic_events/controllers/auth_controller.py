import os
import click
from dotenv import load_dotenv
from jwt import encode, decode, InvalidTokenError
from sqlalchemy import select
from json import load, dump, JSONDecodeError

from epic_events.models import User
from epic_events.views.auth_view import (
    display_successful_connection,
    display_auth_already_connected,
    display_invalid_token,
    display_auth_data_entry_error,
    display_not_connected_error,
)

load_dotenv()
JWT_KEY = os.getenv("JWT_KEY")
TOKEN_FILE_PATH = "auth_token.json"

@click.group()
@click.pass_context
def auth(ctx):
    ctx.ensure_object(dict)

def verify_token(token):
    try:
        return decode(token, JWT_KEY, algorithms=["HS256"])
    except InvalidTokenError:
        return None

def get_token():
    try:
        with open(TOKEN_FILE_PATH, 'r') as f:
            return load(f).get('token')
    except (FileNotFoundError, JSONDecodeError):
        return None

def check_auth(function):
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        session = ctx.obj["session"]
        token = get_token()
        if not token:
            return display_not_connected_error()
        auth_id = verify_token(token)
        if not auth_id:
            return display_invalid_token()
        ctx.obj["current_user"] = session.scalar(select(User).where(User.id == auth_id["id"]))
        return function(ctx, *args, **kwargs)
    return wrapper

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
