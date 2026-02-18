from fastapi import APIRouter,status,HTTPException,Depends
from utilis.db import get_db
from sqlalchemy.orm import Session,joinedload
from sqlalchemy.exc import IntegrityError
from model.userModel import User,role
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from utilis.security import getUser,verifyRole
from model.productModel import Product
from model.userModel import role
from decimal import Decimal



load_dotenv()


router = APIRouter()

class newProduct(BaseModel):
    name:str
    price:float
    description:str
    available:int

class UserOut(BaseModel):
    user_id:UUID
    userName:str
    
    class config:
        from_attributes = True


class ProductOut(BaseModel):
    productId:UUID
    name:str
    price:Decimal
    description : Optional[str]
    vendor:UserOut
    available:int

class ProductUpdate(BaseModel):
    name:Optional[str] = None
    price:Optional[Decimal] = None
    description:Optional[str] = None
    available:Optional[int] = None
    
    class Config:
        from_attributes = True


@router.post("/product/add")
def addProduct(product:newProduct,db:Session=Depends(get_db),user = Depends(verifyRole(role.vendor))):
    try:
        new =Product(
           name = product.name,
           price = product.price,
           description = product.description,
           vendor_id = user.user_id,
           available = product.available
        )
        db.add(new)
        db.commit()
        db.refresh(new)
        return new
        
        
    except IntegrityError as err:
        db.rollback()
        return err


@router.get("/products",response_model=list[ProductOut])
def getProducts(db:Session=Depends(get_db)):
    try:
        products = db.query(Product).options(joinedload(Product.vendor)).all()
        return products
        
    except IntegrityError as err:
        return err


@router.get("/product/{id}",response_model=ProductOut)
def getById(id:UUID,db:Session=Depends(get_db)):
    try:
        product = db.query(Product).options(joinedload(Product.vendor)).filter(Product.productId == id).first()
        return product
        
    except IntegrityError as err:
        return err
    
@router.get("/vendor/product/{id}",response_model=list[ProductOut])
def getVendorProductById(id:UUID,db:Session=Depends(get_db)):
    try:
        vendor = db.query(User).filter(User.user_id == id).first()
        if not vendor:
            raise HTTPException(status_code=404,detail="vendor not found")
        found = db.query(Product).options(joinedload(Product.vendor)).filter(Product.vendor_id == id).all()
        return found
        
    except IntegrityError as err:
        return err

@router.get("/vendor/products")
def getVendorProduct(user = Depends(verifyRole(role.vendor)),db:Session=Depends(get_db)):
    try:
        product = db.query(Product).options(joinedload(Product.vendor)).filter(Product.vendor_id == user.user_id).all()
        return product
        
    except IntegrityError as err:
        return err
    
@router.delete("/product/delete/{id}")
def deleteProduct(id:UUID,db:Session=Depends(get_db),user = Depends(verifyRole(role.vendor,role.admin))):
    try:
        found = db.query(Product).filter(Product.productId == id).first()
        if not found:
            raise HTTPException(status_code=400,details="product not found")
        if found.vendor_id != user.user_id:
            raise HTTPException(status_code=400,details="this user can not delete")
        
        db.delete(found)
        db.commit()
        return "product is deleted"
           
    except IntegrityError as err:
        db.rollback()
        return err
    
@router.patch("/product/update/{id}")
def updateProduct(id:UUID,product:ProductUpdate,db:Session=Depends(get_db),user=Depends(verifyRole(role.vendor))):
    try:
        found = db.query(Product).filter(Product.productId == id).first()
        if not found:
            raise HTTPException(status_code=404,details="product not found")
        if found.vendor_id != user.user_id:
            raise HTTPException(status_code=400,details="user can not update a product")
        
        for key,value in product.model_dump(exclude_unset=True).items():
           setattr(found,key,value)
           
        db.commit()
        db.refresh(found)
        return found
    except IntegrityError as err:
        db.rollback()
        return err
    