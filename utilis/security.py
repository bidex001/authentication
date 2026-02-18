from fastapi import APIRouter,status,HTTPException,Depends
from utilis.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model.userModel import User,role
from jose import jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
from uuid import UUID
from jose.exceptions import ExpiredSignatureError





load_dotenv()

secret = os.getenv("SECRET")
algorithm = "HS256"
expires = 60



def getById(id:str,db:Session=Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id==id).first()
        return user       
    except IntegrityError as err:
        db.rollback()
        return 


oauth = OAuth2PasswordBearer(tokenUrl="login")

def getUser(token = Depends(oauth),db:Session=Depends(get_db)):
    try:
        value = jwt.decode(token,str(secret),algorithms=[algorithm])
    except ExpiredSignatureError as err:
        raise HTTPException(status_code=401,detail="token expired")
        
    id = value["id"]
    found = getById(id,db)
    if not found or isinstance(found,Exception):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")
    if(found.token_version != value["token_version"]):
        raise HTTPException(status_code=400,detail="invalid token")
    return found

def verifyRole(*allowed:role):
    def verify(user:User = Depends(getUser)):
        if(user.role not in allowed):
            raise HTTPException(status_code=404,detail="invalid role")
        return user
    return verify