import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv("local.env")

sql_database_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    database=os.getenv("MYSQL_DATABASE"),
)

engine = create_engine(sql_database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

base = declarative_base()