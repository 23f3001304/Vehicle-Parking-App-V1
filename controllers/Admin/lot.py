from flask import url_for, redirect, session, request
from flask_login import current_user
from utils.sanitizer import sanitize_text, sanitize_address, sanitize_pincode, sanitize_numeric
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.Admin import Admin
from models.ParkingLot import ParkingLot
from models.ParkingSpot import ParkingSpot
import uuid
from .utils.lot_utils import _render_addLot_template, _render_editLot_template

class LotController:
    def __init__(self, db_session, admin_utils):
        self.db_session = db_session
        self.utils = admin_utils
    
    def handle_lot_addition(self):
        """Handle the addition of a new parking lot"""
        if not isinstance(current_user, Admin):
            session["alert_message"] = "You are not authorized to access that page."
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            form_token = request.form.get('form_token')
            stored_token = session.pop('form_token', None)
            
            if stored_token and form_token == stored_token:
                pass
            elif stored_token:
                return redirect(url_for('add_lot'), code=303)
                
            session['form_token'] = str(uuid.uuid4())
            
            location_raw = sanitize_text(request.form.get('prime location', ''))
            location = self.utils._to_title_case(location_raw)
            address = sanitize_address(request.form.get('address', ''))
            pincode = sanitize_pincode(request.form.get('pincode', ''))
            
            price_per_hour = sanitize_numeric(request.form.get('price_per_hour'), min_value=1)
            capacity = sanitize_numeric(request.form.get('maximum spots'), min_value=1)
            
            if not all([location, address, pincode, price_per_hour, capacity]):
                return _render_addLot_template(alert_message="All fields are required", toast=True, form_token=session.get('form_token'))
            
            try:
                if price_per_hour <= 0:
                    return _render_addLot_template(alert_message="Price per hour must be positive", toast=True, form_token=session.get('form_token'))
                
                if capacity <= 0:
                    return _render_addLot_template(alert_message="Maximum spots must be positive", toast=True, form_token=session.get('form_token'))
                new_lot = ParkingLot(
                    uuid=str(uuid.uuid4()),
                    location=location,
                    capacity=capacity,
                    price_per_hour=price_per_hour,
                    address=address,
                    pin_code=pincode,
                    free_spots=capacity,  
                    admin_id=current_user.id
                )
                
                self.db_session.add(new_lot)
                self.db_session.commit()
                
                for i in range(1, capacity + 1):
                    spot = ParkingSpot(
                        spot_number=i,
                        uuid=str(uuid.uuid4()),
                        status=0, 
                        parking_lot_id=new_lot.id
                    )
                    self.db_session.add(spot)
                self.db_session.commit()                
                session['success_message'] = f"Parking lot '{location}' added successfully with {capacity} spots!"
                return redirect(url_for('admin_dashboard'), code=303)
                
            except ValueError:
                return _render_addLot_template(alert_message="Invalid numeric values", toast=True, form_token=session.get('form_token'))
            except IntegrityError as e:
                self.db_session.rollback()
                error_msg = self.utils._parse_integrity_error(e, location)
                return _render_addLot_template(alert_message=error_msg, toast=True, form_token=session.get('form_token'))
            except SQLAlchemyError as e:
                self.db_session.rollback()
                error_msg = f"Database error: {str(e).split(':', 1)[0]}"
                return _render_addLot_template(alert_message=error_msg, toast=True, form_token=session.get('form_token'))
            except Exception as e:
                self.db_session.rollback()
                return _render_addLot_template(alert_message=f"Error adding parking lot: {str(e)}", toast=True, form_token=session.get('form_token'))
        
        session['form_token'] = str(uuid.uuid4())  
        success_message = session.pop('success_message', None)
        alert_message = session.pop('alert_message', None)
        
        if alert_message:
            return _render_addLot_template(alert_message=alert_message, toast=True, form_token=session.get('form_token'))
        
        return _render_addLot_template(success_message=success_message, toast=bool(success_message), form_token=session.get('form_token'))

    def handle_lot_edit(self, encrypted_uuid):
        """Handle the editing of an existing parking lot"""
        if not isinstance(current_user, Admin):
            session["alert_message"] = "You are not authorized to access that page."
            return redirect(url_for('dashboard'))
        
        uuid_str = self.utils.decrypt_uuid(encrypted_uuid)
        if not uuid_str:
            session["alert_message"] = "Parking Lot does not exist or is invalid"
            return redirect(url_for('admin_dashboard'))
            
        lot = self.db_session.query(ParkingLot).filter_by(uuid=uuid_str, admin_id=current_user.id).first()
        
        if not lot:
            session["alert_message"] = "Parking lot not found"
            return redirect(url_for('admin_dashboard'))
        
        if request.method == 'POST':
            # Form validation and processing
            form_token = request.form.get('form_token')
            stored_token = session.pop('form_token', None)
            if stored_token and form_token == stored_token:
                pass
            elif stored_token:
                return redirect(url_for('admin_dashboard'), code=303)  
            session['form_token'] = str(uuid.uuid4())
            
            location_raw = sanitize_text(request.form.get('prime location', ''))
            location = self.utils._to_title_case(location_raw)
            address = sanitize_address(request.form.get('address', ''))
            pincode = sanitize_pincode(request.form.get('pincode', ''))  
            price_per_hour = sanitize_numeric(request.form.get('price_per_hour'), min_value=1)
            capacity = sanitize_numeric(request.form.get('maximum spots'), min_value=1)   
            
            if not all([location, address, pincode, price_per_hour, capacity]):
                return _render_editLot_template(alert_message="All fields are required", toast=True, lot=lot, form_token=session.get('form_token'))
            
            try:
                if price_per_hour <= 0:
                    return _render_editLot_template(alert_message="Price per hour must be positive", toast=True,lot=lot, form_token=session.get('form_token'))
                if capacity <= 0:
                    return _render_editLot_template(alert_message="Maximum spots must be positive", toast=True, lot=lot, form_token=session.get('form_token'))
                if lot.pin_code == pincode and lot.location == location and lot.price_per_hour == price_per_hour and lot.capacity == capacity and lot.address == address:
                    session['alert_message'] = "No changes detected in the parking lot ."
                    return redirect(url_for('admin_dashboard'), code=303)
                if lot.pin_code != pincode:
                    existing_lot = self.db_session.query(ParkingLot).filter_by(pin_code=pincode, admin_id=current_user.id).first()
                    if existing_lot:
                        return _render_editLot_template(alert_message="A parking lot with this pincode already exists. Please use another pincode.", toast=True, lot=lot, form_token=session.get('form_token'))
                    lot.pin_code = pincode
                if lot.location != location:
                    lot.location = location
                if lot.address != address:
                    lot.address = address
                if lot.price_per_hour != price_per_hour:
                    lot.price_per_hour = price_per_hour    
                if lot.capacity < capacity: 
                    change_in_capacity = capacity - lot.capacity
                    for i in range(lot.capacity + 1, capacity + 1):
                        spot = ParkingSpot(
                            spot_number=i,
                            uuid=str(uuid.uuid4()),
                            status=0, 
                            parking_lot_id=lot.id
                        )
                        self.db_session.add(spot)
                    lot.capacity = capacity   
                    lot.free_spots += change_in_capacity
                elif lot.capacity > capacity:
                    change_in_capacity = lot.capacity - capacity
                    spots = self.db_session.query(ParkingSpot).filter_by(parking_lot_id=lot.id).all()
                    free_spots = [spot for spot in spots if spot.status == 0]
                    
                    if len(free_spots) < change_in_capacity:
                        return _render_editLot_template(
                            alert_message="Cannot delete spots that are currently occupied or insufficient free spots to remove",
                            toast=True,
                            lot=lot,
                            form_token=session.get('form_token')
                        )

                    spots_to_delete = free_spots[:change_in_capacity]

                    for spot in spots_to_delete:
                        self.db_session.delete(spot)

                    lot.capacity = capacity
                    lot.free_spots -= change_in_capacity  

                session['success_message'] = f"Parking lot '{location}' updated successfully!"
                self.db_session.commit()

                return redirect(url_for('admin_dashboard'), code=303)
                
            except ValueError:
                return _render_editLot_template(alert_message="Invalid numeric values", toast=True, lot=lot, form_token=session.get('form_token'))
            except IntegrityError as e:
                self.db_session.rollback()
                error_msg = self.utils._parse_integrity_error(e, location)
                return _render_editLot_template(alert_message=error_msg, toast=True, lot=lot, form_token=session.get('form_token'))
            except SQLAlchemyError as e:
                self.db_session.rollback()
                error_msg = f"Database error: {str(e).split(':', 1)[0]}"
                return _render_editLot_template(alert_message=error_msg, toast=True, lot=lot, form_token=session.get('form_token'))
            except Exception as e:
                self.db_session.rollback()
                return _render_editLot_template(alert_message=f"Error updating parking lot: {str(e)}", toast=True, lot=lot, form_token=session.get('form_token'))
        
        if alert_message := session.pop('alert_message', None):
            return _render_editLot_template(alert_message=alert_message, toast=True, lot=lot, form_token=session.get('form_token'))
            
        return _render_editLot_template(lot=lot, form_token=session.get('form_token'))

    def handle_delete_lot(self, encrypted_uuid):
        """Handle the deletion of a parking lot"""
        if not isinstance(current_user, Admin):
            session["alert_message"] = "You are not authorized to access that page."
            return redirect(url_for('dashboard'))
            
        uuid_str = self.utils.decrypt_uuid(encrypted_uuid)
        if not uuid_str:
            session["alert_message"] = "Invalid parking lot identifier"
            return redirect(url_for('admin_dashboard'))
            
        lot = self.db_session.query(ParkingLot).filter_by(uuid=uuid_str, admin_id=current_user.id).first()
        if lot:
            spots = self.db_session.query(ParkingSpot).filter_by(parking_lot_id=lot.id).all()
            if any(spot.status != 0 for spot in spots):
                session["alert_message"] = "Cannot delete parking lot with occupied spots"
                return redirect(url_for('admin_dashboard'))
            self.db_session.delete(lot)
            self.db_session.commit()
        else:
            self.db_session.rollback()
            
        if not lot:
            session["alert_message"] = "Parking lot not found"
            return redirect(url_for('admin_dashboard'))
        
        session['success_message'] = f"Parking lot '{lot.location}' deleted successfully!"
        return redirect(url_for('admin_dashboard'), code=303)