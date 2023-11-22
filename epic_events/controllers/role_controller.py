import click
from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Role
from epic_events.views.base import display_exception
from epic_events.views.base import display_roles_list


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
    Retrieve a list of roles with the "management" permission.

    Args:
        session: The database session.
        ctx: The click context.

    Returns:
        A formatted string displaying the list of roles.

    Raises:
        Exception: If an error occurs while retrieving the roles.
    """
    try:
        roles = session.scalars(select(Role)).all()
        return display_roles_list(roles)
    except Exception as e:
        return display_exception(e)


@role.command(name="create")
def create_role():
    pass
