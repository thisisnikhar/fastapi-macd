from sqlalchemy.orm import relationship

from commons.database import base
from sqlalchemy import Column, String, Integer, ForeignKey


class RequestData(base):
    __tablename__ = "request_data"

    ticket_id = Column(Integer, unique=True, index=True)
    ticket_number = Column(String(25), primary_key=True)
    ticket_type = Column(String(25))

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    ci_onboarding = relationship(
        "CIOnboardingServerData",
        back_populates="request",
        uselist=False,
    )

    tech_onboarding = relationship(
        "TechOnboardingServerData",
        back_populates="request",
        uselist=False,
    )

    users = relationship(
        "Users",
        back_populates="request"
    )
    

class CIOnboardingServerData(base):
    __tablename__ = "ci_onboarding_server_data"
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
        back_populates="ci_onboarding"
    )


class TechOnboardingServerData(base):
    __tablename__ = "tech_onboarding_server_data"
    id = Column(Integer, index=True, primary_key=True)
    record_id = Column(Integer)
    ip_address = Column(String(80), index=True)
    hostname = Column(String(80), index=True)
    tech_name = Column(String(80),nullable=False)
    tech_version = Column(String(10),nullable=False)

    request_id = Column(String(25),ForeignKey("request_data.ticket_number"))

    request = relationship(
        "RequestData",
        back_populates="tech_onboarding"
    )


class Users(base):
    __tablename__ = "users"
    id = Column(Integer,index=True,primary_key=True)
    username = Column(String(25),unique=True,index=True,nullable=False)
    password = Column(String(100),nullable=False)
    email = Column(String(100),index=True,unique=True,nullable=False)
    role = Column(String(20),nullable=False)

    request = relationship(
        "RequestData",
        back_populates="users"
    )

    def __repr__(self):
        return (
            f"Users(id={self.id}, "
            f"username='{self.username}', "
            f"email='{self.email}', "
            f"role='{self.role}')"
        )
