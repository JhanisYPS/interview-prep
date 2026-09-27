from fastapi import Depends, HTTPException
from models.models import engine, User
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from main import oauth2_schema, SECRET_KEY, ALGORITHM


def get_session():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    finally:
        session.close()

def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms = ALGORITHM)
        user_id: int = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Not Authoraized")

    except JWTError as error:
        raise HTTPException(status_code=401, detail=f"Not Authoraized:{error}")

    user = session.get(User, user_id)
    
    return user
