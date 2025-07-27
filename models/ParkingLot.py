from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from .Base import Base  

class ParkingLot(Base):
    __tablename__ = 'parking_lot'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False)
    location = Column(String(100),nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_hour = Column(Integer, nullable=False)
    address = Column(String(100), nullable=False)
    pin_code = Column(String(10), nullable=False)
    free_spots = Column(Integer, nullable=False) 
    revenue_generated = Column(Integer, default=0) 
    admin_id = Column(Integer, ForeignKey('admin.id'), nullable=False)
    admin = relationship("Admin", back_populates="parking_lots")
    parking_spots = relationship("ParkingSpot", back_populates="parking_lot", cascade="all, delete-orphan")    
    
        
    __table_args__ = (
        CheckConstraint('capacity > 0 AND capacity <= 50', name='check_capacity_range'),
        CheckConstraint('price_per_hour > 0 AND price_per_hour <= 1000', name='check_price_range'),
        CheckConstraint('free_spots >= 0', name='check_free_spots_non_negative'),
        CheckConstraint('free_spots <= capacity', name='check_free_spots_leq_capacity'),
        UniqueConstraint('pin_code', 'location', 'address', name='uq_pin_location_address')
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'free_spots' not in kwargs:
            self.free_spots = self.capacity