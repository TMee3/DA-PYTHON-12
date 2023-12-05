import click
import sentry_sdk
from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.permissions import has_permission
from epic_events.models import Role, User
from epic_events.views.generic_view import display_missing_data, display_exception, display_no_data_to_update
from epic_events.views.user_view import display_user_already_exists, display_incorrect_role, display_user_created, \
    display_unknown_user, display_user_data, display_user_updated, display_user_deleted, display_users_list


@click.group()
@click.pass_context
@check_auth
def user(ctx):
    ctx.ensure_object(dict)


@user.command(name="create")
@click.option("-n", "--name", required=True, type=str)
@click.option("-e", "--email", required=True, type=str)
@click.option("-r", "--role", required=True, type=int)
@click.password_option()
@click.pass_context
@has_permission(roles=["management"])
def create_user(session, ctx, name, email, password, role):
    if not (name and email and password and role):
        return display_missing_data()
    if session.scalar(select(User).where(User.email == email)):
        return display_user_already_exists(email)

    user_role = session.scalar(select(Role).where(Role.id == role))
    if not user_role:
        return display_incorrect_role(role)

    try:
        new_user = User(name=name,
                        email=email,
                        role=user_role.id)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()

        # Send a message via sentry to notify that a user is created
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("user-info", "create user")
            sentry_sdk.capture_message("New user created.")

        return display_user_created(email)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return display_exception(e)


@user.command(name="update")
@click.option("-id", "--user_id", required=True, type=int)
@click.option("-n", "--name", required=False, type=str)
@click.option("-e", "--email", required=False, type=str)
@click.option("-r", "--role", required=False, type=int)
@click.pass_context
@has_permission(roles=["management"])
def update_user(session, ctx, user_id, name, email, role):
    if not (name or email or role):
        return display_no_data_to_update()

    selected_role = ""
    if role:
        selected_role = session.scalar(select(Role).where(Role.id == role))
        if not selected_role:
            return display_incorrect_role(role)

    selected_user = session.scalar(select(User).where(User.id == user_id))
    if not selected_user:
        return display_unknown_user()

    try:
        selected_user.name = name if name else selected_user.name
        selected_user.email = email if email else selected_user.email
        selected_user.role = selected_role.id if role else selected_user.role
        session.commit()

        # Send a message via sentry to notify that a user is updated
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("user-info", "update user")
            sentry_sdk.capture_message(f"User {selected_user.id} has been updated.")

        return display_user_updated(selected_user.email)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return display_exception(e)


@user.command(name="get")
@click.option("-id", "--user_id", required=True, type=int)
@click.pass_context
@has_permission(roles=["management"])
def get_user(session, ctx, user_id):
    selected_user = session.scalar(select(User).where(User.id == user_id))
    if not selected_user:
        return display_unknown_user()
    return display_user_data(selected_user)


@user.command(name="delete")
@click.option("-id", "--user_id", required=True, type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this user?")
@click.pass_context
@has_permission(roles=["management"])
def delete_user(session, ctx,  user_id):
    selected_user = session.scalar(select(User).where(User.id == user_id))
    if not selected_user:
        return display_unknown_user()

    try:
        session.delete(selected_user)
        session.commit()
        return display_user_deleted()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return display_exception(e)


@user.command(name="list")
@click.option("-r", "--role_id", required=False, type=int)
@click.pass_context
@has_permission(["management", "commercial", "support"])
def list_users(session, ctx, role_id):
    try:
        query = select(User)
        if role_id:
            selected_role = session.scalar(select(Role).where(Role.id == role_id))
            if not selected_role:
                return display_incorrect_role(role_id)
            query = query.where(User.role == role_id)
        users = session.scalars(query.order_by(User.name))
        return display_users_list(users)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return display_exception(e)
