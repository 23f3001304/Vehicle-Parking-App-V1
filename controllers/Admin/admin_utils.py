from flask import render_template, url_for
import re
import base64
from .utils.getter import _get_spot_fields
from cryptography.fernet import Fernet

class AdminUtils:
    def __init__(self, db_session):
        self.db_session = db_session
        self._cipher = None
    
    @property
    def cipher(self):
        if self._cipher is None:
            from flask import current_app
            secret_key = current_app.config.get('SECRET_KEY')
            key = base64.urlsafe_b64encode(secret_key[:32].encode().ljust(32, b' '))
            self._cipher = Fernet(key)
        return self._cipher
    
    def encrypt_uuid(self, uuid_str):
        if not uuid_str:
            return ""
        return base64.urlsafe_b64encode(self.cipher.encrypt(uuid_str.encode())).decode()
    
    def decrypt_uuid(self, encrypted_str):
        try:
            decoded = base64.urlsafe_b64decode(encrypted_str)
            return self.cipher.decrypt(decoded).decode()
        except Exception as e:
            self.debug_print(f"UUID decryption error: {e}")
            return None
            
    def _to_title_case(self:None, text):
        text = text.strip()
        
        if not text:
            return text
            
        words = [word for word in text.split() if word]
        
        if not words:
            return ""
        
        result = ' '.join(word.capitalize() for word in words)
        
        return result
        
    def _parse_integrity_error(self, error,ll):
        error_str = str(error).lower()
        self.debug_print(f"IntegrityError: {error_str}")
        
        if 'unique constraint failed:' in error_str:
            constraint_part = error_str.split('unique constraint failed:')[1].split('[')[0].strip()
            
            if 'parking_lot.uq_pin_location_address' in constraint_part or 'parking_lot.pin_code' in constraint_part:
                return "A parking lot with this combination of pincode, location and address already exists."
            elif 'parking_lot.uuid' in constraint_part:
                return "System error: UUID collision occurred. Please try again."
        
        if 'unique constraint' in error_str or 'unique violation' in error_str or 'duplicate' in error_str:
            if ('uq_pin_location_address' in error_str) or ('pin_code' in error_str and 'location' in error_str and 'address' in error_str):
                return "A parking lot with this combination of pincode, location and address already exists."
            elif 'uuid' in error_str and 'parking_lot' in error_str:
                return "System error: UUID collision occurred. Please try again."
        
        if 'foreign key constraint' in error_str:
            if 'admin_id' in error_str:
                return "Administrator validation failed. Please contact system support."
            return "Reference error: Required related data is missing."
        
        if 'not null constraint' in error_str or 'null value' in error_str:
            field_mapping = {
                'location': 'Location/Name',
                'capacity': 'Capacity',
                'price_per_hour': 'Price per hour',
                'address': 'Address',
                'pin_code': 'Pincode',
                'free_spots': 'Available spots',
                'admin_id': 'Administrator'
            }
            
            for db_field, display_name in field_mapping.items():
                if db_field in error_str:
                    return f"The {display_name} field cannot be empty."
        
        if 'invalid input syntax' in error_str:
            if 'integer' in error_str:
                return "Please enter valid numbers for capacity and price."
            
        return "Unable to save parking lot due to a database constraint violation."
    
    def debug_print(self, message):
        """Safe debug printing that doesn't expose sensitive details"""
        if isinstance(message, str):
            safe_message = re.sub(r'(password|token|key|secret)=\S+', r'\1=[REDACTED]', message, flags=re.IGNORECASE)
            print(f"[DEBUG] {safe_message}")
        else:
            print(f"[DEBUG] {type(message)}")
            
            
    def _render_viewSpot_template(self, alert_message=None, success_message=None, toast=False, spot=None, form_token=None,encrypted_uuid=None):
        page_title = "View - " + str(spot.id) + " spot - ParkEase"
        page_title1 = "Parking Spot Details"
        image_path = "/static/images/spot.png"
        
        icon_map = {
            'id': 'svg/id.svg',
            'spot': 'svg/spots.svg',
            'status': 'svg/status.svg',
        }
        from models import ParkingLot
        from db import db_session
        lot = db_session.query(ParkingLot).filter_by(id=spot.parking_lot_id).first()
        lot_encrypted_uuid = self.encrypt_uuid(lot.uuid) if lot else ''
        back_link_path = f'/admin/lot/{lot_encrypted_uuid}/spots'
        
        fields =  _get_spot_fields(spot)
        return render_template('forms/form.html',
                              back_link=back_link_path,
                              alert_message=alert_message,
                              success_message=success_message,
                              toast=toast,
                              fields=fields,
                              button_text="Delete",
                              button_class="login-button",
                              button_id="parking-button",
                              type='parking_spot',
                              reservation_path= f'/admin/reservation/{encrypted_uuid}',                           
                              image_path=image_path,
                              icon_map=icon_map,
                              Page_title=page_title,
                              Page_title1=page_title1,
                              form_token=form_token)