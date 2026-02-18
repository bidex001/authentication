from utilis.db import Base
from sqlalchemy import Integer,Column,String,DateTime,func,Enum as sqlEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import Mapped,mapped_column,relationship
from enum import Enum

class role(str,Enum):
    admin = "admin"
    customer = "customer"
    vendor = "vendor"


class User(Base):
    __tablename__="users"
    user_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    userName = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    otp = Column(Integer,nullable=True)
    otpExpiry = Column(DateTime(timezone=True),nullable=True)
    role : Mapped[role] = mapped_column(
        sqlEnum(role,name="role_enum"),default=role.customer,nullable=False
    )
    products = relationship("Product",back_populates="vendor",cascade="all,delete")
    cart = relationship("Cart",back_populates = "user",cascade="all,delete-orphan")
    token_version: Mapped[int] = mapped_column(default=0)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())