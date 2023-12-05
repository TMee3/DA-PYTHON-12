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

if __name__ == "__main__":
    session = current_session()
