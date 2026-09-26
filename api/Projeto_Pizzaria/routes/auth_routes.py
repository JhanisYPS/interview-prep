from fastapi import APIRouter, Depends, HTTPException
from models.models import User
from dependencies.dependencies import get_session

from main import bcrypt_context
from schemas.schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

#função auxiliar
def create_token(user_id:int):
    token = f"ahdushduah{user_id}sudha"
    return token

def auth_user(email:str, password: str, session: Session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    else:
        return user

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

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = auth_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="user not found")
    else:
        access_token = create_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

