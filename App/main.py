from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routes import users, notes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message" : "Secure Notes API running successfully"}