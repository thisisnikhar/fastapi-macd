from sqlalchemy.orm import relationship

from commons.database import base
from sqlalchemy import Column, String, Integer, ForeignKey


class RequestData(base):
    __tablename__ = "request_data"
    ticket_id = Column(Integer, index=True, unique=True)
    ticket_number = Column(String(25), index=True, primary_key=True)

    server_data = relationship("ServerData",back_populates="request")


class ServerData(base):
    __tablename__ = "server_data"
    id = Column(Integer, index=True, primary_key=True)
    record_id = Column(Integer)
    ip_address = Column(String(80), index=True)
    hostname = Column(String(80), index=True)
    serial_number = Column(String(80), index=True)
    operating_system = Column(String(80))
    os_version = Column(String(80))
    cpu = Column(Integer)
    memory = Column(Integer)
    hard_disk = Column(Integer)

    request_id = Column(String(25), ForeignKey("request_data.ticket_number"))

    request = relationship(
        "RequestData",
        back_populates="server_data"
    )
