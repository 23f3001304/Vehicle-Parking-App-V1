import re
import html
import unicodedata

def sanitize_text(text, max_length=None):

    if text is None:
        return ""
        
    text = str(text)
    
    text = unicodedata.normalize('NFKC', text)
    
    text = text.strip()
    
    text = html.escape(text)
    
    if max_length and len(text) > max_length:
        text = text[:max_length]
        
    return text

def sanitize_email(email, max_length=100):

    if email is None:
        return ""
        
    email = str(email)
    
    email = email.lower()
    
    email = "".join(email.split())
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return ""
        
    if max_length and len(email) > max_length:
        email = email[:max_length]
        
    email = html.escape(email)
    
    return email

def sanitize_pincode(pincode):

    if pincode is None:
        return ""
        
    pincode = str(pincode)
    
    digits_only = ''.join(c for c in pincode if c.isdigit())
    
    if len(digits_only) != 6:
        return ""
        
    return digits_only

def sanitize_numeric(value, min_value=None, max_value=None):
    try:
        num = int(value)
        
        if min_value is not None and num < min_value:
            num = min_value
        if max_value is not None and num > max_value:
            num = max_value
            
        return num
    except (ValueError, TypeError):
        return None

def sanitize_name(name, max_length=50):
    if name is None:
        return ""
        
    name = str(name)
    name = unicodedata.normalize('NFKC', name)
    
    name = " ".join(name.split())
    
    name = re.sub(r'[^\w\s\'-]', '', name, flags=re.UNICODE)
    
    name = " ".join(word.capitalize() for word in name.split())
    
    if max_length and len(name) > max_length:
        name = name[:max_length]
        
    name = html.escape(name)
    
    return name

def sanitize_address(address, max_length=200):
    if address is None:
        return ""
        
    address = str(address)
    address = unicodedata.normalize('NFKC', address)
    
    address = " ".join(address.split())
    
    address = re.sub(r'[^\w\s,.#()\-/]', '', address, flags=re.UNICODE)
    
    if max_length and len(address) > max_length:
        address = address[:max_length]
        
    address = html.escape(address)
    
    return address
