from jose import jwt, JWTError 
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import schemas
import database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import schema
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRETE_KEY =  settings.secret_key 
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def varify_access_token(token: str, creadentials_exception):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id == None:
            raise creadentials_exception
        token_data = schemas.TokenData(user_id=id)
    except JWTError:
        raise creadentials_exception
    return token_data
   
def get_current_user(token: str = Depends(oauth2_scheme), db: Session =  Depends(database.get_db)):
    creadentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = varify_access_token(token, creadentials_exception)
    user = db.query(models.User).filter(models.User.id == token.user_id).first()
    return user
   