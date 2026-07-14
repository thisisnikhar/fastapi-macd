from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


sql_database_url = "mysql+pymysql://root:Admin%40123@127.0.0.1:3306/macd"
# %40 represents @

engine = create_engine(sql_database_url)
SessionLocal = sessionmaker(bind=engine,autoflush=False)

base = declarative_base()
