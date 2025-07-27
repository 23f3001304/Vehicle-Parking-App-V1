# models/reservation.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, validates
from .Base import Base
import re
from datetime import datetime

class Reservation(Base):
    __tablename__ = 'reservation'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    parking_spot_id = Column(Integer, ForeignKey('parking_spot.id'), nullable=False)
    vehicle_number = Column(String(20), nullable=False)
    start_time = Column(String(30), nullable=False)
    end_time = Column(String(30), nullable=True)
    status = Column(Integer, nullable=False)
    current_cost = Column(Float, default=0.0)

    user = relationship("User", back_populates="reservations")
    parking_spot = relationship("ParkingSpot", back_populates="reservations")

    @validates('vehicle_number')
    def validate_vehicle_number(self, key, value):
        pattern = r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$'
        if not re.match(pattern, value):
            raise ValueError("Invalid vehicle number format")
        return value

    @validates('status')
    def validate_status(self, key, value):
        self.calculate_cost()
        return value

    def get_duration(self):
        start = datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S") if self.end_time else datetime.now()
        return (end - start).total_seconds() / 3600

    def calculate_cost(self, rate_per_hour=None):
        """Calculate current cost based on duration and the parking lot's rate"""
        if rate_per_hour is None:
            try:
                from models.ParkingSpot import ParkingSpot
                from models.ParkingLot import ParkingLot
                
                if hasattr(self, '_sa_instance_state') and self._sa_instance_state.session_id:
                    session = self._sa_instance_state.session
                    spot = session.query(ParkingSpot).filter_by(id=self.parking_spot_id).first()
                    if spot:
                        lot = session.query(ParkingLot).filter_by(id=spot.parking_lot_id).first()
                        if lot:
                            rate_per_hour = lot.price_per_hour
                else:
                    rate_per_hour = 50
            except Exception:
                rate_per_hour = 50
        
        duration = self.get_duration()
        self.current_cost = round(duration * rate_per_hour, 2)
        return self.current_cost
