from functools import wraps

from sqlalchemy import select

from epic_events.models import Role
from epic_events.views.permissions_view import display_not_authorized


def has_permission(roles):
    def decorator(function):
        @wraps(function)
        def wrapper(ctx, *args, **kwargs):
            session = ctx.obj["session"]
            current_user = ctx.obj["current_user"]
            selected_roles = [session.scalar(select(Role.id).where(Role.name == role)) for role in roles]
            if current_user.role not in selected_roles:
                return display_not_authorized()
            return function(session, ctx, *args, **kwargs)
        return wrapper
    return decorator
