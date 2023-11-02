from sqlalchemy import Column, Integer, String
from database.db import Base

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    # Add other fields here