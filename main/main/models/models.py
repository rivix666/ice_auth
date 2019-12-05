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
    access = relationship('IcecastAccess')
    active_listeners = relationship('ActiveListeners')

    def accessParams(self):
        if len(self.access) != 1:
            #TODO dodac log z liczba accessow
            return None
        return self.access[0]

    def countActiveListeners(self):
        return len(self.active_listeners)

# Index('listeners_index', Listeners.id, unique=True, mysql_length=255)


class IcecastAccess(Base):
    __tablename__ = 'icecast_access'
    id = Column(Integer, primary_key=True)
    listener_id = Column(Integer, ForeignKey('listeners.id'), unique=True)  
    max_listeners = Column(Integer)
    expiration_date = Column(Date)


#  Index('icecast_access_index', IcecastAccess.listener_id,
#        unique=True, mysql_length=255)


class ActiveListeners(Base):
    __tablename__ = 'active_listeners'
    id = Column(Integer, primary_key=True)
    listener_id = Column(Integer, ForeignKey('listeners.id'), unique=True)
    addresses = relationship('ListenersAddresses')


class ListenersAddresses(Base):
    __tablename__ = 'listeners_addresses'
    id = Column(Integer, primary_key=True)
    listener_id = Column(Integer, ForeignKey('active_listeners.id'), unique=True)  
    listener_ip = Column(Text)
    active_listeners = relationship('ActiveListeners')
    # listener_mac = Column(Text) #zoabczyc czy da sie w ogole wydobyc i ew dorobic mechanizm do banowania 

# Index('icecast_access_index', ActiveListeners.listener_id,
#        unique=True, mysql_length=255)
