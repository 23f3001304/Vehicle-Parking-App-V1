from sqlalchemy import Column, Integer, String
from .Base import Base
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class Admin(Base, UserMixin):
    __tablename__ = 'admin'
    
    id = Column(String(10), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    parking_lots = relationship("ParkingLot", back_populates="admin", foreign_keys="ParkingLot.admin_id")




