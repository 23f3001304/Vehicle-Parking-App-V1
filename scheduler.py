import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from db import Session
from models.Reservation import Reservation
from models.ParkingSpot import ParkingSpot
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('cost_scheduler')
def update_costs():
    start_time = datetime.now()
    session = Session()
    count = 0
    try:
        reservations = (
            session.query(Reservation)
            .filter_by(status=1)
            .options(
                joinedload(Reservation.parking_spot)
                .joinedload(ParkingSpot.parking_lot)
            )
            .all()
        )
        for reservation in reservations:
            try:
                price_per_hour = reservation.parking_spot.parking_lot.price_per_hour
                reservation.calculate_cost(rate_per_hour=price_per_hour)
                count += 1
            except Exception as e:
                logger.error(f"Error updating cost for reservation {reservation.id}: {e}")
        
        session.commit()
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Updated costs for {count} active reservations in {elapsed:.2f}s")
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error updating costs: {e}")
    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error updating costs: {e}")
    finally:
        session.close()

def start_scheduler():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            update_costs, 
            'interval', 
            seconds=10,
            id='cost_update_job',
            replace_existing=True,
            max_instances=1,
            coalesce=True  
        )
        scheduler.start()
        logger.info("Cost update scheduler started successfully (10s interval)")
        return scheduler
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        return None
