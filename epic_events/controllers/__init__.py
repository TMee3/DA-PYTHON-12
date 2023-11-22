import click

from .user_controller import user

from .role_controller import role
from .auth_controller import auth
from ..database import current_session


@click.group()
@click.pass_context
def cli(ctx):
    """
    This function initializes the command line interface (CLI) for the Epic Events application.
    
    Parameters:
        ctx (click.Context): The click context object.
    
    Returns:
        None
    """
    ctx.ensure_object(dict)
    ctx.obj["session"] = current_session()


cli.add_command(user)
cli.add_command(role)
cli.add_command(auth)
