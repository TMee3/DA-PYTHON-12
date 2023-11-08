from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Collaborator(Base):
    __tablename__ = 'collaborator'
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    role_id = Column(Integer, ForeignKey('role.id'))
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(255))
    telephone = Column(String(25))
    role = relationship("Role")

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    enterprise_name = Column(String(255))
    create_date = Column(Date)
    last_update_date = Column(Date)
    contact_id = Column(Integer, ForeignKey('collaborator.id'))
    contact = relationship("Collaborator")

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(String(1000))
    attendees = Column(Integer)
    comments = Column(String(1000))
    support_id = Column(Integer, ForeignKey('collaborator.id'))
    contract_id = Column(Integer, ForeignKey('contract.id'))
    support = relationship("Collaborator", foreign_keys=[support_id])
    contract = relationship("Contract")

class Contract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True)
    legal_id = Column(String(255))
    price = Column(Float)
    remaining_to_pay = Column(Float)
    create_date = Column(Date)
    status = Column(String(255))
    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship("Client")
