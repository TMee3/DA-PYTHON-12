import click
import sentry_sdk

from epic_events.controllers.auth_controller import auth
from epic_events.controllers.client_controller import client
from epic_events.controllers.contract_controller import contract
from epic_events.controllers.event_controller import event
from epic_events.controllers.role_controller import role
from epic_events.controllers.user_controller import user
from epic_events.database import current_session


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
        sentry_sdk.capture_exception(e)
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

if __name__ == "__main__":
    cli()
