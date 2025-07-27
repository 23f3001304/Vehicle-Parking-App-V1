import base64
from cryptography.fernet import Fernet
from flask import current_app

class BaseController:    
    def __init__(self, db_session):
        self.db_session = db_session
        self._cipher = None
        
    @property
    def cipher(self):
        if self._cipher is None:
            secret_key = current_app.config.get("SECRET_KEY")
            key = base64.urlsafe_b64encode(secret_key[:32].encode().ljust(32, b" "))
            self._cipher = Fernet(key)
        return self._cipher
    
    def encrypt_uuid(self, uuid_str):
        if not uuid_str:
            return ""
        return base64.urlsafe_b64encode(self.cipher.encrypt(str(uuid_str).encode())).decode()
    
    def decrypt_uuid(self, encrypted_str):
        try:
            decoded = base64.urlsafe_b64decode(encrypted_str)
            return self.cipher.decrypt(decoded).decode()
        except Exception as e:
            return None

    def _to_title_case(self, text):
        if not text:
            return text
            
        text = text.strip()
        words = [word for word in text.split() if word]
        
        if not words:
            return ""
        
        return ' '.join(word.capitalize() for word in words)
