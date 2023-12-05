from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from epic_events.models import Role, User
from epic_events.models.base import Base


def current_session():
    load_dotenv()
    db_url = getenv("DB_URL")
    assert db_url is not None, "DB_URL must be set, see the .env.example"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        return s


def insert_initial_data(session):
    roles = session.scalars(select(Role)).all()
    if not roles:
        commercial = Role(name="commercial")
        support = Role(name="support")
        management = Role(name="management")

        session.add_all([commercial, support, management])
        session.commit()

        role = session.scalar(select(Role).where(Role.name == "management"))
        load_dotenv()
        first_user_password = getenv("FIRST_USER_PASSWORD")
        first_user_email = getenv("FIRST_USER_EMAIL")
        first_user_name = getenv("FIRST_USER_NAME")
        first_user = User(name=first_user_name, email=first_user_email, role=role.id)

        first_user.set_password(first_user_password)

        session.add(first_user)
        session.commit()


if __name__ == "__main__":
    session = current_session()
    insert_initial_data(session)
