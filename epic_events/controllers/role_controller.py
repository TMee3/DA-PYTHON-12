import click
import sentry_sdk
from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.models import Role
from epic_events.permissions import has_permission
from epic_events.views.generic_view import display_exception
from epic_events.views.role_view import display_roles_list

""" Role controller"""


@click.group()
@click.pass_context
@check_auth
def role(ctx):
    ctx.ensure_object(dict)


""" List all roles """


@role.command(name="list")
@click.pass_context
@has_permission(["management"])
def list_roles(session, ctx):
    try:
        roles = session.scalars(select(Role)).all()
        return display_roles_list(roles)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return display_exception(e)
