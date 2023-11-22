from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from epic_events.models import Role, User
from epic_events.models.base import Base


def current_session():

    db_url = "sqlite:///epic_events.db"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    session = Session(engine)
    return session


def start_user_insert(session):
    roles = [
        Role(name="commercial"),
        Role(name="support"),
        Role(name="management")
    ]
    session.add_all(roles)
    session.commit()

    role = session.scalar(select(Role).where(Role.name == "management"))

    first_user_password = "admin"
    first_user_email = "admin@admin.fr"
    first_user_name = "admin"
    first_user = User(name=first_user_name, email=first_user_email, role=role.id)
    print(first_user)

    first_user.set_password(first_user_password)
    session.add(first_user)
    session.commit()


if __name__ == "__main__":
    print("Starting user insert")
    session = current_session()
    start_user_insert(session)
    print("User insert finished")
