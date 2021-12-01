from fastapi import APIRouter, Depends, HTTPException, status, Response 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from database import get_db
import schemas
import models 
import utils
import oauth2 

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token, status_code=status.HTTP_200_OK)
async def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not utils.varify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
