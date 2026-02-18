from fastapi import APIRouter,status,HTTPException,Depends
from utilis.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model.userModel import User,role
from pydantic import BaseModel
from typing import Optional
from utilis.crypt import hashPassword,verify
from utilis.generateJwt import createToken
import os
from jose import jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from utilis.security import getUser,verifyRole
import random
from datetime import datetime,timedelta,timezone
from model.cartModel import Cart


load_dotenv()

secret = os.getenv("SECRET")
algorithm = "HS256"
expires = 60





class NewUser(BaseModel):
    username:str
    email:str
    password:str

class loginUser(BaseModel):
    email:str
    password:str


class otpConfirm(BaseModel):
    otp:int

class UserOut(BaseModel):
    user_id : UUID
    otp : int
    role : str

    class Config:
        from_attributes = True


def createCart(id,db:Session):
    newCart = Cart(
        user_id = id
    )
    db.add(newCart)
    db.commit()
    
    
    


router = APIRouter()

oauth = OAuth2PasswordBearer(tokenUrl="login")

def getUser(token = Depends(oauth),db:Session=Depends(get_db)):
    value = jwt.decode(token,str(secret),algorithms=[algorithm])
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
    


@router.post("/user/add")
def createUser(user:NewUser,db:Session= Depends(get_db)):
    try:
        NewUser = User(
            userName=user.username,
            email=user.email,
            password=hashPassword(user.password),
            role = role.customer 
        )
        db.add(NewUser)
        db.commit()
        createCart(NewUser.user_id,db)
        db.refresh(NewUser)
        return "user and cart created"
        
    except IntegrityError as err:
        db.rollback()
        return err
    
    
@router.post("/user/login")
def login(user:loginUser,db:Session=Depends(get_db)):
    try:
        found = db.query(User).filter(User.email==user.email).first()
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
        checkPassword = verify(user.password,found.password)
        if not checkPassword:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid password")
        
        token = createToken({"id":str(found.user_id),"token_version":found.token_version})
        return token
        
    except IntegrityError as err:
        db.rollback()
        return err
    
    
@router.get("/users")
def getUsers(db:Session=Depends(get_db)):
    try:
        user = db.query(User).all()
        return user
        
    except IntegrityError as err:
        db.rollback()
        return err
    
    
@router.get("/user/me")
def getCurrentUser(user = Depends(getUser)):
    return user
    
@router.get("/user/{id}")
def getById(id:str,db:Session=Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id==id).first()
        return user       
    except IntegrityError as err:
        db.rollback()
        return 

    
    
@router.patch("/users/promote/{id}")
def promoteUser(id:UUID, user:User = Depends(verifyRole(role.admin)), db:Session = Depends(get_db)):
    try:
        found = db.query(User).filter(User.user_id == id).first()
        if not found:
            raise HTTPException(status_code=404,detail="user not found")
        found.role = role.admin
        db.commit()
        db.refresh(found)
        return found
    except IntegrityError as err:
        db.rollback()
        return err
    
    
# for otp message
@router.patch("/users/upgrade",response_model=UserOut)
def upgradeUser(db:Session=Depends(get_db),user=Depends(verifyRole(role.customer))):
    try:
        otp = random.randint(1000,9999)
        user.otp = otp
        user.otpExpiry = datetime.now(timezone.utc) + timedelta(minutes=5)
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError as err:
        db.rollback()
        return err


# for otp confirmation
@router.post("/user/otp/confirm")
def confirmOtp(payload:otpConfirm,db:Session=Depends(get_db),user = Depends(verifyRole(role.customer))):
    try:
        if payload.otp != user.otp:
            raise HTTPException(status_code=404,detail="invalid otp")
        if user.otpExpiry < datetime.now(timezone.utc):
            raise HTTPException(status_code=404,detail="otp expired")

        user.role = role.vendor
        db.commit()
        db.refresh(user)
        return user


    except IntegrityError as err:
        db.rollback()
        return err
