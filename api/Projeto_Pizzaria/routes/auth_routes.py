from fastapi import APIRouter, Depends
from models.models import User
from dependencies.dependencies import get_session

from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def get_auth():
    """Endpoint for authentication. Returns a message indicating the authentication endpoint."""
    return {"message": "Authentication endpoint"}

@auth_router.post("/create_account")
async def post_create_account(name:str, email: str, password: str, session = Depends(get_session)):

    user = session.query(User).filter(User.email==email).first()
    if user:
        return {'mensage': "user alredy existe"}
    else:
        crypt_password = bcrypt_context.hash(password)
        new_user = User(name= name, email=email, password=crypt_password)
        session.add(new_user)
        session.commit()
        return {'mensage': "user created"}

