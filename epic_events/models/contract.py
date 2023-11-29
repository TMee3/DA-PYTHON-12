from datetime import datetime, timezone
from typing import Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.models.base import Base

Status = Literal["SIGNED", "UNSIGNED"]


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))
    total_amount: Mapped[int]
    left_to_pay: Mapped[int]
    status: Mapped[Status]
    creation_date: Mapped[datetime] = mapped_column(insert_default=datetime.now(timezone.utc))
    update_date: Mapped[datetime] = mapped_column(insert_default=datetime.now(timezone.utc),
                                                  onupdate=datetime.now(timezone.utc))
    client = relationship("Client", back_populates="contracts")
    events = relationship("Event", back_populates="contract", cascade="all, delete")

    def __repr__(self):
        return f"Contract(id={self.id}, client_id={self.client_id}, status={self.status})"
