# MACD Portal Backend

A REST API backend built with **FastAPI** for managing server onboarding requests, user authentication, and ticket management. The application provides JWT-based authentication, role-based authorization, and separate workflows for CI and Technology onboarding.

## Features

- JWT-based authentication
- Role-based authorization (Admin/User)
- User management and login
- CI onboarding request management
- Technology onboarding request management
- Automatic ticket generation
- MySQL database integration
- SQLAlchemy ORM
- Alembic database migrations
- Pydantic request and response validation
- Integration testing with Pytest
- Separate test database
- Dockerized application deployment

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Programming language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| SQLAlchemy | ORM and database operations |
| MySQL | Relational database |
| Alembic | Database migrations |
| Pydantic | Data validation |
| Passlib / bcrypt | Password hashing |
| Python-Jose | JWT authentication |
| Pytest | Integration testing |
| Docker | Application containerization |

## Project Structure

```text
.
├── routers/
│   ├── users.py
│   ├── ci_onboarding.py
│   ├── tech_onboarding.py
│   └── macd.py
├── commons/
│   ├── auth.py
│   ├── database.py
│   ├── db_dependency.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_auth.py
│   ├── test_ci_onboarding.py
│   ├── test_tech_onboarding.py
│   └── test_macd.py
├── alembic/
├── main.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## API Modules

### Users
- Create users
- Authenticate users
- Retrieve usernames

### CI Onboarding
- Create CI onboarding requests
- Retrieve the current user's requests
- Retrieve all requests (Admin)

### Technology Onboarding
- Create technology onboarding requests
- Retrieve the current user's requests
- Retrieve all requests (Admin)

## Authentication and Authorization

The application uses **JSON Web Tokens (JWT)** to authenticate users.

Passwords are hashed using bcrypt before being stored in the database.

Protected endpoints require a bearer token:

```http
Authorization: Bearer <access_token>
```

### Roles

**Admin**
- Create and manage users, where permitted by the API
- View all onboarding requests
- Access administrative endpoints

**User**
- Authenticate
- Create onboarding requests
- View their own requests

## Database

- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic

Apply database migrations with:

```bash
alembic upgrade head
```

Configure the database connection using environment variables or your application's configuration mechanism. Do not commit database credentials to the repository.

## Installation and Local Development

### 1. Clone the repository

```bash
git clone https://github.com/thisisnikhar/fastapi-macd.git
cd fastapi-macd
```

### 2. Create a virtual environment

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the database

Ensure MySQL is running and create the application database.

Configure the database URL using the mechanism expected by the application. Example format:

```text
mysql+pymysql://<username>:<password>@<host>:3306/<database_name>
```

Keep credentials and secret keys outside version control.

### 5. Apply migrations

```bash
alembic upgrade head
```

### 6. Start the application

```bash
uvicorn main:app --reload
```

The application will be available at:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Docker

Build the Docker image from the directory containing the Dockerfile:

```bash
docker build -t fastapi-macd:0.0.1 .
```

Run the container:

```bash
docker run --name fastapi-macd -p 8000:5000 fastapi-macd:0.0.1
```

This port mapping assumes the application listens on port `5000` inside the container. Adjust the mapping if your Uvicorn configuration uses a different port.

**Database connectivity:** The application container must be able to reach MySQL. If MySQL runs in another container, connect both containers to a shared Docker network and use the database container or service name as the hostname. If MySQL runs on the host machine, configure the appropriate host address.

Provide database credentials and JWT secrets through environment variables or another secure configuration mechanism. Do not bake secrets into the image.

## Testing

A dedicated MySQL test database is used for integration testing.

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run with coverage, if `pytest-cov` is installed:

```bash
pytest --cov=. --cov-report=term-missing
```

### Test Coverage Areas

- User creation and login
- JWT authentication
- Role-based authorization
- CI onboarding APIs
- Technology onboarding APIs
- Protected endpoints
- Database operations

## Security

- Password hashing using bcrypt
- JWT-based authentication
- Role-based authorization
- Request validation using Pydantic
- Parameterized database operations through SQLAlchemy ORM

For production deployments, configure strong secrets, validate authorization rules, and use secure environment configuration.

## Future Enhancements

- Refresh tokens
- Password reset
- Email notifications
- Audit logging
- Automated CI/CD pipeline
- Kubernetes deployment
- AWS deployment

## Author

**Nikhar Sachdeva**

Backend Developer

**Technologies:** Python, FastAPI, SQLAlchemy, MySQL, REST APIs, Docker