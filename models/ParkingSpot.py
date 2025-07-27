from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base

class ParkingSpot(Base):
    __tablename__ = 'parking_spot'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False)
    spot_number = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    parking_lot_id = Column(Integer, ForeignKey('parking_lot.id'), nullable=False)
     
    parking_lot = relationship("ParkingLot", back_populates="parking_spots")
    reservations = relationship("Reservation", back_populates="parking_spot", cascade="all, delete-orphan")