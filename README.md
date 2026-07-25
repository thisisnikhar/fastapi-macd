# MACD Portal Backend

A backend REST API built with **FastAPI** for managing server onboarding requests, user authentication, and ticket management. The application provides secure JWT-based authentication, role-based authorization, and separate workflows for CI and Technology onboarding.

---

## Features

- JWT Authentication
- Role-based Authorization (Admin/User)
- User Management
- CI Onboarding Requests
- Technology Onboarding Requests
- Automatic Ticket Generation
- MySQL Database Integration
- SQLAlchemy ORM
- Alembic Database Migrations
- Pydantic Request & Response Validation
- Integration Testing using Pytest
- Separate Test Database

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.x | Programming Language |
| FastAPI | REST API Framework |
| SQLAlchemy | ORM |
| MySQL | Database |
| Alembic | Database Migrations |
| Pydantic | Data Validation |
| Passlib (bcrypt) | Password Hashing |
| Python-Jose | JWT Authentication |
| Pytest | Integration Testing |
| Uvicorn | ASGI Server |

---

## Project Structure

```text
.
├── routers/
│   ├── users.py
│   ├── ci_onboarding.py
│   ├── tech_onboarding.py
│   └── macd.py
│
├── commons/
│   ├── auth.py
│   ├── database.py
│   ├── db_dependency.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
│
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_auth.py
│   ├── test_ci_onboarding.py
│   ├── test_tech_onboarding.py
│   └── test_macd.py
│
├── alembic/
├── main.py
├── requirements.txt
└── README.md
```

---

# API Modules

## Users

- Create User
- Login
- Get All Usernames

---

## CI Onboarding

- Create CI Onboarding Request
- Get Current User Requests
- Get All Requests (Admin)

---

## Technology Onboarding

- Create Technology Onboarding Request
- Get Current User Requests
- Get All Requests (Admin)

---

## Authentication

The application uses **JWT (JSON Web Tokens)** for authentication.

Passwords are securely hashed using **bcrypt** before storing them in the database.

Protected endpoints require the following header:

```http
Authorization: Bearer <access_token>
```

---

## Roles

### Admin

- Create Users
- View all onboarding requests
- Access administrative APIs

### User

- Login
- Create onboarding requests
- View own requests

---

# Database

Database: **MySQL**

ORM: **SQLAlchemy**

Database migrations are managed using **Alembic**.

---

# Installation

## Clone the repository

```bash
git clone https://github.com/<your-username>/<repository-name>.git

cd <repository-name>
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Database

Update your database connection inside the project configuration.

Example:

```python
mysql+pymysql://username:password@localhost/database_name
```

---

## Run Alembic Migrations

```bash
alembic upgrade head
```

---

## Start the Application

```bash
uvicorn main:app --reload
```

Application will be available at:

```
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Running Tests

A dedicated MySQL test database is used for integration testing.

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov=. --cov-report=term-missing
```

---

# Test Coverage

The project includes integration tests for:

- User Creation
- User Login
- JWT Authentication
- Role-based Authorization
- CI Onboarding APIs
- Technology Onboarding APIs
- Protected Endpoints
- Database Operations

---

# Security

- Passwords hashed using bcrypt
- JWT Authentication
- Role-based Authorization
- Request validation using Pydantic
- SQL Injection protection through SQLAlchemy ORM

---

# Future Enhancements

- Refresh Tokens
- Password Reset
- Email Notifications
- Audit Logging
- Docker Support
- CI/CD Pipeline
- Kubernetes Deployment
- AWS Deployment

---

# Author

**Nikhar Sachdeva**

Backend Developer

**Tech Stack**

- Python
- FastAPI
- Flask
- Django
- Core Java
- SQLAlchemy
- MySQL
- AWS
- REST APIs

---
