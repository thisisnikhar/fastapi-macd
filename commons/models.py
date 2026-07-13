from commons.database import base
from sqlalchemy import Column,String,Integer


class RequestData(base):
    __tablename__ = "request_data"
    ticket_id = Column(Integer, index=True, unique=True)
    ticket_number = Column(String(25), index=True, primary_key=True)
