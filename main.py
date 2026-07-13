from fastapi import FastAPI
from commons.database import base,engine


app = FastAPI()

base.metadata.create_all(bind=engine)
