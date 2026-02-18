from utilis.db import Base
from sqlalchemy import Integer,Column,String,DateTime,func,Enum as sqlEnum,ForeignKey,DECIMAL
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import Mapped,mapped_column,relationship
from enum import Enum




class Product(Base):
    __tablename__="products"
    productId = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column (String,nullable=False)
    price = Column (DECIMAL,nullable=False)
    description = Column(String,nullable=True)
    available:Mapped[int] = mapped_column(default=1,nullable=False)
    vendor_id = Column(UUID(as_uuid=True),ForeignKey("users.user_id"),nullable=False)
    vendor = relationship("User",back_populates="products")