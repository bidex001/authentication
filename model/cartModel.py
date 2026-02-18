from utilis.db import Base
from sqlalchemy import Integer,Column,String,DateTime,func,Enum as sqlEnum,ForeignKey,DECIMAL
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import Mapped,mapped_column,relationship
from enum import Enum


class Cart(Base):
   __tablename__ = "carts"
   id = Column(UUID,primary_key = True,default=uuid.uuid4)
   user_id = Column(UUID(as_uuid=True),ForeignKey("users.user_id"),nullable=False)
   user = relationship("User",back_populates="cart")
   items = relationship("CartItem",back_populates="cart",cascade="all,delete-orphan")
   
   
class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True),ForeignKey("products.productId"),nullable=False)
    quantity = Column(Integer) 
    cart_id = Column(UUID(as_uuid=True),ForeignKey("carts.id"),nullable=False)
    cart = relationship("Cart",back_populates="items")