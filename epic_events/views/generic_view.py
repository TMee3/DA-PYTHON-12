from click import ClickException


def display_missing_data():
    raise ClickException("Missing data in the command")


def display_exception(e):
    raise ClickException(f"Error: {e}") from e


def display_no_data_to_update():
    raise ClickException("Can't update without data in the command.")
