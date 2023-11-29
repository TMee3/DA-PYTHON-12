from click import ClickException


def display_user_already_exists(email):
    raise ClickException(f"User ({email}) already exists.")


def display_incorrect_role(role):
    raise ClickException(f"{role} is not a correct role.")


def display_user_created(email):
    print(f"User {email} is successfully created")


def display_unknown_user():
    raise ClickException("Sorry, this user does not exist.")


def display_user_data(data):
    print(data)


def display_user_updated(email):
    print(f"User {email} is successfully updated")


def display_user_deleted():
    print("This user is successfully deleted")


def display_users_list(users):
    for user in users:
        print(f"Id: {user.id}, name: {user.name}, email: {user.email}, role: {user.role}")
