import click

from .user_controller import user
from .client_controller import client
from .contract_controller import contract
from .event_controller import event
from .role_controller import role
from .auth_controller import auth
from ..database import current_session


@click.group(help="This tool manages the Epic Events application.")
@click.pass_context
def cli(ctx):
    """
    Initializes the main CLI group and the shared session for database interaction.
    """
    ctx.ensure_object(dict)
    
    try:
        ctx.obj["session"] = current_session()
    except Exception as e:
        click.echo("Failed to initialize database session.", err=True)
        click.echo(str(e), err=True)
        ctx.exit(1)

# Add commands to the CLI group
cli.add_command(user) 
cli.add_command(client)
cli.add_command(contract)
cli.add_command(event)
cli.add_command(role)
cli.add_command(auth)

if __name__ == '__main__':
    cli()
