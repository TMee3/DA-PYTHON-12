import click
from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.permissions import has_permission
from epic_events.models import Role
from epic_events.views.generic_view import display_exception
from epic_events.views.role_view import display_roles_list


@click.group()
@click.pass_context
@check_auth
def role(ctx):
    ctx.ensure_object(dict)


@role.command(name="list")
@click.pass_context
@has_permission(["management"])
def list_roles(session, ctx):
    """
    Retrieve a list of roles and display them.

    Args:
        session: The database session.
        ctx: The click context.

    Returns:
        The formatted list of roles.

    Raises:
        Exception: If an error occurs during the retrieval or display of roles.
    """
    try:
        roles = session.execute(select(Role)).scalars().all()
        return display_roles_list(roles)
    except Exception as e:
        return display_exception(e)
