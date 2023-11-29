from click import ClickException


def display_not_authorized():
    raise ClickException("Sorry, you're not authorized.")
