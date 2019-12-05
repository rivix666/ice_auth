from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Date,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from .meta import Base

class Listeners(Base):
    __tablename__ = 'listeners'
    id = Column(Integer, primary_key=True)
    uuid = Column(Text, unique=True)
    access = relationship('IcecastAccess', cascade="all,delete")
    active_listeners = relationship('ActiveListeners')

class IcecastAccess(Base):
    __tablename__ = 'icecast_access'
    id = Column(Integer, primary_key=True)
    listener_id = Column(Integer, ForeignKey('listeners.id'), unique=True)  
    max_listeners = Column(Integer)
    expiration_date = Column(Date)

class ActiveListeners(Base):
    __tablename__ = 'active_listeners'
    id = Column(Integer, primary_key=True)
    listener_id = Column(Integer, ForeignKey('listeners.id'), unique=True)
    listener_ip = Column(Text)
    # listener_mac = Column(Text) # TODO Check if we need that 
