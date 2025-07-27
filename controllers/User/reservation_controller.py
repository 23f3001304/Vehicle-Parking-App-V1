from flask import request, redirect, url_for, render_template, session
from flask_login import current_user
from datetime import datetime
import re
import uuid
from controllers.base_controller import BaseController
from models import ParkingLot, ParkingSpot, Reservation
from sqlalchemy.orm import joinedload


class ReservationController(BaseController):
    
    def __init__(self, db_session):
        super().__init__(db_session)
    
    def _get_book_fields(self, lot, spot=None):
        fields = [
            {'name': 'lot_location', 'label': 'PRIME LOCATION', 'type': 'text', 'icon': 'Location', 'value': lot.location, 'disabled': True},
            {'name': 'lot_address', 'label': 'ADDRESS', 'type': 'text', 'icon': 'Address', 'value': lot.address, 'disabled': True},
        ]
        
        if spot:
            fields.append({'name': 'spot', 'label': 'SPOT NUMBER', 'type': 'number', 'icon': 'Capacity', 'value': spot.spot_number, 'disabled': True})
            
        fields.append({'name': 'vehicle_number', 'label': 'VEHICLE NUMBER', 'type': 'text', 'icon': 'Vehicle', 'placeholder': 'e.g., MH02AB1234'})
        
        return fields
    
    def _render_book_template(self, lot, alert_message=None, success_message=None, toast=False, form_token=None, spot=None):
        page_title = f"Book Spot - ParkEase"
        page_title1 = f"Book a Spot "
        image_path = "/static/images/spot.png"
        
        icon_map = {
            'Location': 'svg/map.svg',
            'Address': 'svg/Address.svg',
            'Capacity': 'svg/spots.svg',
            'Price': 'svg/price.svg',
            'Vehicle': 'svg/car.svg'
        }
        
        fields = self._get_book_fields(lot, spot)
        
        return render_template('forms/form.html',
                              back_link=url_for('dashboard'),
                              alert_message=alert_message,
                              success_message=success_message,
                              toast=toast,
                              fields=fields,
                              button_text="BOOK NOW",
                              button_class="login-button",
                              button_id="booking-button",
                              type='book_lot',
                              url=url_for('book_spot', lot_uuid=self.encrypt_uuid(lot.uuid)),
                              image_path=image_path,
                              icon_map=icon_map,
                              Page_title=page_title,
                              Page_title1=page_title1,
                              form_token=form_token)
    
    def handle_book_lot(self, lot_uuid):
        
        lot_uuid = self.decrypt_uuid(lot_uuid)
        if not lot_uuid:
            session["alert_message"] = "Invalid parking lot UUID."
            return redirect(url_for("dashboard"))
        
        lot = (
            self.db_session.query(ParkingLot)
            .filter(ParkingLot.uuid == lot_uuid)
            .first()
        )
        
        if not lot:
            session["alert_message"] = "Parking lot not found."
            return redirect(url_for("dashboard"))
        
        if lot.free_spots <= 0:
            session["alert_message"] = "No free spots available in this parking lot."
            return redirect(url_for("dashboard"))
        
        free_spot = (
            self.db_session.query(ParkingSpot)
            .filter(ParkingSpot.parking_lot_id == lot.id, ParkingSpot.status == 0)
            .first()
        )
        
        if not free_spot:
            session["alert_message"] = "No free spots available in this parking lot."
            return redirect(url_for("dashboard"))
        
        if request.method == "POST":
            form_token = request.form.get('form_token')
            stored_token = session.pop('form_token', None)
            
            if stored_token and form_token == stored_token:
                pass
            elif stored_token:
                return redirect(url_for('book_spot', lot_uuid=self.encrypt_uuid(lot.uuid)), code=303)
                    
            session['form_token'] = str(uuid.uuid4())
            
            vehicle_number = request.form.get("vehicle_number", "").strip().upper()
            
            if not vehicle_number:
                return self._render_book_template(
                    lot=lot,
                    spot=free_spot,
                    alert_message="Vehicle number is required.",
                    toast=True,
                    form_token=session.get('form_token')
                )
            
            vehicle_pattern = r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{1,4}$'
            if not re.match(vehicle_pattern, vehicle_number):
                return self._render_book_template(
                    lot=lot,
                    spot=free_spot,
                    alert_message="Invalid vehicle number format. Use format like MH02AB1234.",
                    toast=True,
                    form_token=session.get('form_token')
                )
            
            existing_active_reservation = (
                self.db_session.query(Reservation)
                .filter(
                    Reservation.vehicle_number == vehicle_number,
                    Reservation.end_time.is_(None),
                    Reservation.status == 1
                )
                .first()
            )
            
            if existing_active_reservation:
                return self._render_book_template(
                    lot=lot,
                    spot=free_spot,
                    alert_message="This vehicle is already parked in another spot.",
                    toast=True,
                    form_token=session.get('form_token')
                )
            
            current_spot_status = self.db_session.query(ParkingSpot.status).filter_by(id=free_spot.id).scalar()
            if current_spot_status != 0:
                new_free_spot = (
                    self.db_session.query(ParkingSpot)
                    .filter(ParkingSpot.parking_lot_id == lot.id, ParkingSpot.status == 0)
                    .first()
                )
                
                if not new_free_spot:
                    session["alert_message"] = "Sorry, all spots were taken while you were filling the form."
                    return redirect(url_for("dashboard"))
                    
                free_spot = new_free_spot
                spot_changed = True
            else:
                spot_changed = False
            
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_reservation = Reservation(
                uuid=str(uuid.uuid4()),
                user_id=current_user.id,
                parking_spot_id=free_spot.id,
                vehicle_number=vehicle_number,
                start_time=now,
                end_time=None,
                status=1  
            )
            
            try:
                free_spot.status = 1
                
                lot.free_spots -= 1
                
                self.db_session.add(new_reservation)
                self.db_session.commit()
                
                if spot_changed:
                    session["success_message"] = f"Your initial spot was taken. New spot #{free_spot.spot_number} booked successfully for vehicle {vehicle_number}."
                else:
                    session["success_message"] = f"Spot #{free_spot.spot_number} booked successfully for vehicle {vehicle_number}."
                return redirect(url_for("dashboard"))
            
            except Exception as e:
                self.db_session.rollback()
                return self._render_book_template(
                    lot=lot,
                    spot=free_spot,
                    alert_message=f"Error booking spot: {str(e)}",
                    toast=True,
                    form_token=session.get('form_token')
                )
        
        session['form_token'] = str(uuid.uuid4())
        return self._render_book_template(
            lot=lot,
            spot=free_spot,
            form_token=session.get('form_token')
        )
    
    def handle_end_reservation(self, res_uuid):
        
        uuid_str = self.decrypt_uuid(res_uuid)
        if not uuid_str:
            session["alert_message"] = "Invalid reservation identifier"
            return redirect(url_for("dashboard"))
            
        reservation = (
            self.db_session.query(Reservation)
            .options(
                joinedload(Reservation.parking_spot)
                .joinedload(ParkingSpot.parking_lot)
            )
            .filter(
                Reservation.uuid == uuid_str,
                Reservation.user_id == current_user.id,
                Reservation.status == 1,
                Reservation.end_time.is_(None)
            )
            .first()
        )
        
        if not reservation:
            session["alert_message"] = "Reservation not found or already ended"
            return redirect(url_for("dashboard"))
            
        try:
            spot = reservation.parking_spot
            lot = spot.parking_lot
            
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            reservation.end_time = end_time
            
            final_cost = reservation.calculate_cost(rate_per_hour=lot.price_per_hour)
            reservation.status = 0
            spot.status = 0
            lot.free_spots += 1
            
            start = datetime.strptime(reservation.start_time, "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            duration_seconds = (end - start).total_seconds()
            hours = int(duration_seconds // 3600)
            minutes = int((duration_seconds % 3600) // 60)
            lot.revenue_generated += final_cost
            self.db_session.commit()
            
            session["success_message"] = (
                f"Reservation ended successfully. "
                f"Duration: {hours}h {minutes}m. "
                f"Total cost: ₹{final_cost:.2f}. "
                f"Thank you for using ParkEase!"
            )
            
            return redirect(url_for("dashboard"))
            
        except Exception as e:
            self.db_session.rollback()
            session["alert_message"] = f"Error ending reservation: {str(e)}"
            return redirect(url_for("dashboard"))