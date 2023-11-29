from functools import wraps
from json import dump, load
from json.decoder import JSONDecodeError
from os import getenv

import click
from dotenv import load_dotenv
from jwt import encode, decode, InvalidTokenError
from sqlalchemy import select

from epic_events.models import User
from epic_events.views.auth_view import display_successful_connection, \
    display_auth_already_connected, display_invalid_token, display_auth_data_entry_error, display_not_connected_error

load_dotenv()
JWT_KEY = getenv("JWT_KEY")
TOKEN_FILE_PATH = "auth_token.json"


@click.group()
@click.pass_context
def auth(ctx):
    ctx.ensure_object(dict)


def verify_token(token):
    """
    Verify the validity of the JWT token
    """
    return decode(token, JWT_KEY, algorithms=["HS256"])


def get_token():
    """
    Retrieve the JWT token from the configuration file
    """
    try:
        with open(TOKEN_FILE_PATH, 'r') as f:
            data = load(f)
            return data.get('token', None)
    except JSONDecodeError as e:
        return None
    except FileNotFoundError:
        return None
    except Exception as e:
        return None


def check_auth(function):
    """
    Decorator to check user authentication
    """
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
            return function(ctx, *args, ** kwargs)
        except InvalidTokenError as e:
            return display_invalid_token()
    return wrapper


@auth.command()
@click.option("-e", "--email", required=True, type=str)
@click.password_option()
@click.pass_context
def login(ctx, email, password):
    """
    Command to log in to the application
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
    """
    Command to log out of the application
    """
    with open(TOKEN_FILE_PATH, "r") as f:
        data = load(f)
        del data["token"]
    with open(TOKEN_FILE_PATH, "w") as f:
        dump(data, f)
    return display_successful_connection(login=False)
