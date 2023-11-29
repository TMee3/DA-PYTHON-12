from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from epic_events.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password = mapped_column(String())
    role: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, role={self.role})"

    def set_password(self, password):
        password_hasher = PasswordHasher()
        self.password = password_hasher.hash(password)

    def check_password(self, password):
        password_hasher = PasswordHasher()
        try:
            password_hasher.verify(self.password, password)
            return True
        except VerifyMismatchError:
            return False
