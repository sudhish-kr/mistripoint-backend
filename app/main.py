from fastapi import FastAPI
from app.database import Base, engine
from app.models.user import User
from app.routes import auth
from app.models.user import User
from app.models.service_request import ServiceRequest
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def home():
    return {
        "message": "MistriPoint Backend Running"
    }