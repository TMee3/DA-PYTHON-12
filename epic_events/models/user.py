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

    password_hasher = PasswordHasher()

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, role={self.role})"

    def set_password(self, password):
        """
        Hashes and sets the user's password.

        Args:
            password (str): The plaintext password to be hashed and set.
        """
        self.password = self.password_hasher.hash(password)

    def check_password(self, password):
        """
        Checks if the provided password matches the user's hashed password.

        Args:
            password (str): The plaintext password to be checked.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        try:
            self.password_hasher.verify(self.password, password)
            return True
        except VerifyMismatchError:
            return False
