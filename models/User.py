from sqlalchemy import Column, Integer, String
from .Base import Base
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    reservations = relationship(
        "Reservation",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )