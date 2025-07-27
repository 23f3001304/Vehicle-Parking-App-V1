from flask import render_template, url_for, redirect, session, request
from flask_login import current_user
from models import Admin, ParkingLot, ParkingSpot, Reservation
from datetime import datetime

class SpotController:
    def __init__(self, db_session, admin_utils):
        self.db_session = db_session
        self.utils = admin_utils
    
    def handle_view_spots(self, encrypted_uuid):
        """Handle the viewing of spots in a parking lot"""
        if not isinstance(current_user, Admin):
            session["alert_message"] = "You are not authorized to access that page."
            return redirect(url_for('dashboard'))
            
        uuid_str = self.utils.decrypt_uuid(encrypted_uuid)
        if not uuid_str:
            session["alert_message"] = "Invalid parking lot identifier"
            return redirect(url_for('admin_dashboard'))
            
        lot = self.db_session.query(ParkingLot).filter_by(uuid=uuid_str, admin_id=current_user.id).first()
        if not lot:
            session["alert_message"] = "Parking lot not found"
            return redirect(url_for('admin_dashboard'))
            
        spots_raw = self.db_session.query(ParkingSpot).filter_by(parking_lot_id=lot.id).all()
        spots = []
        for spot in spots_raw:
            spot_data = {
                'id': spot.id,
                'uuid': self.utils.encrypt_uuid(spot.uuid),
                'spot_number': spot.spot_number,
                'status': spot.status,
                'parking_lot_id': spot.parking_lot_id,
            }
            spots.append(spot_data)
            
        
        lot_data = {
            'title': lot.location,
            'capacity': lot.capacity,
            'free': lot.free_spots,
            'price': lot.price_per_hour,
            'address': lot.address + ", " + lot.pin_code,
            'occupied': lot.capacity - lot.free_spots,
            'expected_revenue': lot.revenue_generated,
            'edit_path': url_for('edit_lot', lot_uuid=self.utils.encrypt_uuid(lot.uuid)),
        }
        
        return render_template('admin/spot_details.html',
                              lot=lot_data,
                              spots=spots)
    
    def handle_view_spot(self, encrypted_uuid):
        if not isinstance(current_user, Admin):
            session["alert_message"] = "You are not authorized to access that page."
            return redirect(url_for('dashboard'))
            
        uuid_str = self.utils.decrypt_uuid(encrypted_uuid)
        if not uuid_str:
            session["alert_message"] = "Invalid parking spot identifier"
            return redirect(url_for('admin_dashboard'))
            
        spot = self.db_session.query(ParkingSpot).filter_by(uuid=uuid_str).first()
        if not spot:
            session["alert_message"] = "Parking spot not found"
            return redirect(url_for('admin_dashboard'))
            
        lot = self.db_session.query(ParkingLot).filter_by(id=spot.parking_lot_id).first()
        if not lot:
            session["alert_message"] = "Parking lot for this spot not found"
            return redirect(url_for('admin_dashboard'))
            
        return self.utils._render_viewSpot_template(spot=spot, form_token=self.utils.encrypt_uuid(spot.uuid),encrypted_uuid = encrypted_uuid) 


    def _get_reservation_fields(self, reservation):
        return {
            'id': reservation.id,
            'uuid': self.utils.encrypt_uuid(reservation.uuid),
            'vehicle_number': reservation.vehicle_number,
            'spot_number': reservation.parking_spot.spot_number,
            'start_time': reservation.start_time,
            'end_time': reservation.end_time.strftime("%Y-%m-%d %H:%M:%S") if reservation.end_time else "Not ended",
            'status': "Active" if reservation.status == 1 else "Ended",
            'current_cost': reservation.current_cost,
        }
        
    def _render_viewReservation_template(self, reservation, alert_message=None, success_message=None, toast=False, form_token=None,encrypted_uuid=None,):
        page_title = f"Reservation Details - ParkEase Admin"
        page_title1 = f"Reservation Details"
        image_path = "/static/images/lot.png"
        
        fields = [
            {'name': 'vehicle_number', 'label': 'VEHICLE NUMBER', 'type': 'text', 'icon': 'Vehicle', 'value': reservation['vehicle_number'], 'disabled': True},
            {'name': 'spot_number', 'label': 'SPOT NUMBER', 'type': 'text', 'icon': 'Capacity', 'value': reservation['spot_number'], 'disabled': True},
            {'name': 'start_time', 'label': 'START TIME', 'type': 'text', 'icon': 'Calendar', 'value': reservation['start_time'], 'disabled': True},
            {'name': 'status', 'label': 'STATUS', 'type': 'text', 'icon': 'Status', 'value': reservation['status'], 'disabled': True},
            {'name': 'current_cost', 'label': 'CURRENT COST', 'type': 'text', 'icon': 'Price', 'value': f"₹{reservation['current_cost']:.2f}", 'disabled': True},
        ]
        
        if reservation['status'] != "Active":
            fields.append({'name': 'end_time', 'label': 'END TIME', 'type': 'text', 'icon': 'Calendar', 'value': reservation['end_time'], 'disabled': True})
        
        icon_map = {
            'Vehicle': 'svg/car.svg',
            'Capacity': 'svg/spots.svg',
            'Calendar': 'svg/calendar.svg',
            'Status': 'svg/status.svg',
            'Price': 'svg/price.svg'
        }
        
        return render_template('forms/form.html',
                           back_link=url_for('admin_dashboard'),
                           alert_message=alert_message,
                           success_message=success_message,
                           toast=toast,
                           fields=fields,
                           type='view_reservation',
                           reservation_path= f'/admin/reservation/{encrypted_uuid}',                           
                           image_path=image_path,
                           icon_map=icon_map,
                           Page_title=page_title,
                           Page_title1=page_title1,
                           form_token=form_token,
                           read_only=True)
    
    def handle_view_reservation(self, encrypted_uuid):
        if not isinstance(current_user, Admin):
            session["alert_message"] = "You are not authorized to access that page."
            return redirect(url_for('dashboard'))
            
        uuid_str = self.utils.decrypt_uuid(encrypted_uuid)
        spot = self.db_session.query(ParkingSpot).filter_by(uuid=uuid_str).first()
        if not uuid_str:
            session["alert_message"] = "Invalid reservation identifier"
            return redirect(url_for('admin_dashboard'))
            
        reservation = self.db_session.query(Reservation).filter_by(parking_spot_id = spot.id , status = 1 ).first()
        
        if not reservation:
            session["alert_message"] = "Reservation not found"
            return redirect(url_for('admin_dashboard'))
            
        if not spot:
            session["alert_message"] = "Parking spot for this reservation not found"
            return redirect(url_for('admin_dashboard'))
            
        lot = self.db_session.query(ParkingLot).filter_by(id=spot.parking_lot_id).first()
        if not lot:
            session["alert_message"] = "Parking lot for this spot not found"
            return redirect(url_for('admin_dashboard'))
        
        current_cost = 0
        if reservation.status == 1:
            start = reservation.start_time
            start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            duration_seconds = (current_time - start).total_seconds()
            hours = duration_seconds / 3600
            current_cost = hours * lot.price_per_hour
            reservation.current_cost = current_cost
        
        reservation_data = self._get_reservation_fields(reservation)
        
        return self._render_viewReservation_template(
            reservation=reservation_data,
            form_token=None, 
            encrypted_uuid = encrypted_uuid
        )