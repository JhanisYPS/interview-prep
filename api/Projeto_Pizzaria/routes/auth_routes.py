from fastapi import APIRouter, Depends, HTTPException
from models.models import User
from dependencies.dependencies import get_session

from main import bcrypt_context
from schemas.schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def get_auth():
    """Endpoint for authentication. Returns a message indicating the authentication endpoint."""
    return {"message": "Authentication endpoint"}

@auth_router.post("/create_account")
async def post_create_account(user_schema: UserSchema, session: Session = Depends(get_session)):

    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="user alredy exist")
    else:
        crypt_password = bcrypt_context.hash(user_schema.password)
        new_user = User(name= user_schema.name, email=user_schema.email, password=crypt_password, active=user_schema.active, admin=user_schema.admin )
        session.add(new_user)
        session.commit()
        return {'mensage': "user created"}

