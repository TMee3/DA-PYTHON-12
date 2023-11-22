import click
from sqlalchemy import select
from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Role, User
from epic_events.views.base import (
    display_exception, display_missing_data, display_user_already_exists,
    display_incorrect_role, display_user_created, display_no_data_to_update,
    display_unknown_user, display_user_data, display_user_updated,
    display_user_deleted, display_users_list
)

@click.group()
@click.pass_context
@check_auth
def user(ctx):
    ctx.ensure_object(dict)

@user.command(name="create")
@click.pass_context
@has_permission(roles=["management"])
def create_user(session, ctx):
    try:
        name = click.prompt("Name", type=str)
        email = click.prompt("Email", type=str)
        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
        role = click.prompt("Role", type=int)
        
        if not (name and email and password and role):
            return display_missing_data()
        
        existing_user = session.scalar(select(User).where(User.email == email))
        if existing_user:
            return display_user_already_exists(email)
        
        user_role = session.scalar(select(Role).where(Role.id == role))
        if not user_role:
            return display_incorrect_role(role)
        
        new_user = User(name=name, email=email, role=user_role.id)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()
        return display_user_created(email)
    except Exception as e:
        return display_exception(e)

@user.command(name="update")
@click.option("-id", "--user_id", required=True, type=int, prompt=True)
@click.pass_context
@has_permission(roles=["management"])
def update_user(session, ctx, user_id):
    """
    Update a user's information.

    Args:
        session: The database session.
        ctx: The click context.
        user_id (int): The ID of the user to update.

    Returns:
        str: A message indicating the success or failure of the update.
    """
    try:
        if not user_id:
            return display_missing_data()
        
        selected_user = session.scalar(select(User).where(User.id == user_id))
        
        if not selected_user:
            return display_unknown_user()
        
        name = click.prompt("Name", type=str, default=selected_user.name)
        email = click.prompt("Email", type=str, default=selected_user.email)
        role = click.prompt("Role", type=int, default=selected_user.role.id)
        
        selected_role = session.scalar(select(Role).where(Role.id == role))
        
        if role and not selected_role:
            return display_incorrect_role(role)
        
        if name:
            selected_user.name = name
        if email:
            selected_user.email = email
        if role:
            selected_user.role = selected_role.id
        
        session.commit()
        return display_user_updated(selected_user.email)
    except Exception as e:
        return display_exception(e)

@user.command(name="get")
@click.option("-id", "--user_id", required=True, type=int, prompt=True)
@click.pass_context
@has_permission(roles=["management"])
def get_user(session, ctx, user_id):
    try:
        if not user_id:
            return display_missing_data()
        
        selected_user = session.scalar(select(User).where(User.id == user_id))
        
        if not selected_user:
            return display_unknown_user()
        
        return display_user_data(selected_user)
    except Exception as e:
        return display_exception(e)

@user.command(name="delete")
@click.option("-id", "--user_id", required=True, type=int, prompt=True)
@click.confirmation_option(prompt="Are you sure you want to delete this user?")
@click.pass_context
@has_permission(roles=["management"])
def delete_user(session, ctx, user_id):
    try:
        selected_user = session.scalar(select(User).where(User.id == user_id))
        
        if not selected_user:
            return display_unknown_user()
        
        session.delete(selected_user)
        session.commit()
        return display_user_deleted()
    except Exception as e:
        return display_exception(e)

@user.command(name="list")
@click.option("-r", "--role_id", required=False, type=int, prompt=False, show_default=True)
@click.pass_context
@has_permission(roles=["management", "commercial", "support"])
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
        return display_exception(e)

if __name__ == "__main__":
    user()
