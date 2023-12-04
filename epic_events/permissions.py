from functools import wraps

from sqlalchemy import select

from epic_events.models import Role
from epic_events.views.generic_view import display_not_authorized


def has_permission(roles):
    """
    Checks if the user has permission to access a function based on their roles.
    :param roles: List of allowed roles
    :return: Function decorator
    """
    def decorator(function):
        @wraps(function)
        def wrapper(ctx, *args, **kwargs):
            session = ctx.obj["session"]
            current_user = ctx.obj["current_user"]
            
            # Get the IDs of the selected roles
            selected_roles = [session.scalar(select(Role.id).where(Role.name == role)) for role in roles]
            
            # Check if the current user's role is in the selected roles
            if current_user.role not in selected_roles:
                return display_not_authorized()
            
            # Call the function with the arguments and keywords
            return function(session, ctx, *args, **kwargs)
        
        return wrapper
    
    return decorator
