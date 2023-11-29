from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from epic_events.models.base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    def __repr__(self):
        return f"Role(id={self.id}, name={self.name})"
