from fastapi import APIRouter,status,HTTPException,Depends
from utilis.db import get_db
from sqlalchemy.orm import Session,joinedload
from sqlalchemy.exc import IntegrityError

from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from utilis.security import getUser
from model.cartModel import Cart,CartItem
from model.userModel import User
from model.productModel import Product

router = APIRouter()

class product_type(BaseModel):
    id:UUID
    quantity:int
    

@router.get("/cart")
def getCart(db:Session=Depends(get_db),user = Depends(getUser)):
    try:
        found = db.query(Cart).options(joinedload(Cart.items)).filter(Cart.user_id == user.user_id).first()
        if not found:
            raise HTTPException(status_code=404,detail="cart not found")
        return found
    except IntegrityError as err:
        return err
    
@router.post("/add/cart")
def addToCart(product:product_type,db:Session=Depends(get_db),user = Depends(getUser)):
    try:
        found = db.query(Cart).filter(Cart.user_id == user.user_id).first()
        if not found:
            raise HTTPException(status_code=404,detail="cart not found")
        
        for item in found.items:
            if item.item_id == product.id:
                raise HTTPException(status_code=400,detail="item already exists in cart")
            
            
        productInStore = db.query(Product).filter(Product.productId == product.id).first()
        if not productInStore :
            raise HTTPException(status_code=404,detail="product not found")
        
        if productInStore.available < product.quantity:
            raise HTTPException(status_code=400,detail="request exceed limit")
        
        newItem = CartItem(
            item_id = product.id,
            quantity = product.quantity,
            cart_id = found.id
        )
        db.add(newItem)
        db.commit()
        db.refresh(newItem)
        return newItem
    except IntegrityError as err:
        db.rollback()
        return err
    
@router.delete("/cart/delete/{id}")
def deleteCart(id,db:Session = Depends(get_db),user = Depends(getUser)):
    try:
        item = db.query(CartItem).options(joinedload(CartItem.cart)).filter(CartItem.id == id).first()
        if not item:
            raise HTTPException(status_code=404,detail="item not found")
        if  item.cart.user_id != user.user_id:
            raise HTTPException(status_code=404,detail="this user can not delete this item")
            
        db.delete(item)
        db.commit()
        return "item is deleted"  
        
    except IntegrityError as err:
        db.rollback()
        return err
    
@router.patch("/cart/update")
def updateCart(q:product_type,db:Session=Depends(get_db),user=Depends(getUser)):
    try:
        item = db.query(CartItem).options(joinedload(CartItem.cart)).filter(CartItem.id == q.id).first()
        if not item :
            raise HTTPException(status_code=404,detail="item not found")
        
        productInStore = db.query(Product).filter(Product.productId ==  item.item_id).first()
        if not productInStore :
            raise HTTPException(status_code=404,detail="product not found")
        
        if productInStore.available < q.quantity:
            raise HTTPException(status_code=400,detail="request exceed limit")
        item.quantity = q.quantity
        db.commit()
        db.refresh(item)
        return item
        
    except IntegrityError as err:
        db.rollback()
        return err
    

    