from commons.models import RequestData,CIOnboardingServerData,TechOnboardingServerData
from sqlalchemy import select,func
from datetime import datetime


def generate_new_ci_id(db):
    query = select(func.max(CIOnboardingServerData.id))
    max_id = db.execute(query).scalar()
    if max_id is None:
        new_id = 1
    else:
        new_id = int(max_id) + 1
    return new_id


def generate_new_tech_id(db):
    query = select(func.max(TechOnboardingServerData.id))
    max_id = db.execute(query).scalar()
    if max_id is None:
        new_id = 1
    else:
        new_id = int(max_id) + 1
    return new_id


def generate_new_ticket_id_and_ticket_number(db):
    query = select(func.max(RequestData.ticket_id))
    max_ticket_id = db.execute(query).scalar()
    if max_ticket_id is None:
        ticket_id = 1
    else:
        ticket_id = int(max_ticket_id) + 1

    year = datetime.now().strftime("%y")  # 26
    ticket_number = f"SR-{year}-{ticket_id:05d}"

    return ticket_id,ticket_number


def add_ci_onboarding_server_data(server_data,db,ticket_number):
    new_id = generate_new_ci_id(db)
    record_id = 1
    for data in server_data:
        data = data.model_dump()  # JSON Request Data to dictionary

        # Updating CIOnboardingServerData Table
        ci_onboarding_server_data = CIOnboardingServerData(
            id=new_id,
            record_id=record_id,
            ip_address=data.get("ip_address"),
            hostname=data.get("hostname"),
            serial_number=data.get("serial_number"),
            operating_system=data.get("operating_system"),
            os_version=data.get("os_version"),
            cpu=data.get("cpu"),
            memory=data.get("memory"),
            hard_disk=data.get("hard_disk"),
            request_id=ticket_number
        )
        db.add(ci_onboarding_server_data)
        new_id = new_id + 1
        record_id = record_id + 1



def add_tech_onboarding_server_data(tech_data,ticket_number,db):
    new_id = generate_new_tech_id(db)
    record_id = 1
    for data in tech_data:
        data = data.model_dump()  # JSON Request Data to dictionary

        # Updating TechOnboardingServerData Table
        tech_onboarding_server_data = TechOnboardingServerData(
            id=new_id,
            record_id=record_id,
            ip_address=data.get("ip_address"),
            tech_type=data.get("tech_type"),
            tech_name=data.get("tech_name"),
            tech_version=data.get("tech_version"),
            request_id=ticket_number
        )
        db.add(tech_onboarding_server_data)
        new_id = new_id + 1
        record_id = record_id + 1


def generate_ci_response_data(requests):
    response = []
    for req in requests:
        server_data = []
        for server in req.ci_onboarding:
            server_data.append(
                {
                    "record_id": server.record_id,
                    "ip_address": server.ip_address,
                    "hostname": server.hostname,
                    "serial_number": server.serial_number,
                    "operating_system": server.operating_system,
                    "os_version": server.os_version,
                    "cpu": server.cpu,
                    "memory": server.memory,
                    "hard_disk": server.hard_disk
                }
            )
        response.append(
            {
                "ticket_number": req.ticket_number,
                "ticket_type": req.ticket_type,
                "username": req.users.username,
                "user_email": req.users.email,
                "server_data": server_data
            }
        )
    return response


def generate_tech_response_data(requests):
    response = []
    for req in requests:
        server_data = []
        for server in req.tech_onboarding:
            server_data.append(
                {
                    "record_id": server.record_id,
                    "ip_address": server.ip_address,
                    "tech_type": server.tech_type,
                    "tech_name": server.tech_name,
                    "tech_version": server.tech_version
                }
            )
        response.append(
            {
                "ticket_number": req.ticket_number,
                "ticket_type": req.ticket_type,
                "username": req.users.username,
                "user_email": req.users.email,
                "server_data": server_data
            }
        )
    return response