from datetime import datetime
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.models.base import Base

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id", ondelete="CASCADE"))
    support_contact_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    start_date: Mapped[datetime] = mapped_column(nullable=True)
    end_date: Mapped[datetime] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    attendees: Mapped[int] = mapped_column(nullable=True)
    notes: Mapped[str] = mapped_column(nullable=True)
    
    creation_date: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow())
    update_date: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    
    contract = relationship("Contract", back_populates="events")

    def __repr__(self):
        return f"Event(id={self.id}, contract_id={self.contract_id}, support_contact_id={self.support_contact_id})"
