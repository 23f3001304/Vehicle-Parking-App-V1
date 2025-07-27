from flask import request, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from utils.sanitizer import sanitize_email, sanitize_name, sanitize_address, sanitize_pincode
from models import User, Admin

class AuthController:
    def __init__(self, db_session):
        self.db_session = db_session  

    def handle_login(self):
        if session.get('alert_message'):
            alert_message = session.pop('alert_message')
            return render_template('auth/login.html', alert_message=alert_message, toast=True, form_token=session.get('form_token'))
        if current_user.is_authenticated:
            if isinstance(current_user, Admin):
                return redirect(url_for('admin/dashboard'))
            else:
                return redirect(url_for('dashboard'))

        if request.method == 'POST':
            form_token = request.form.get('form_token')
            stored_token = session.pop('form_token', None)
            
            if stored_token and form_token == stored_token:
                pass
            elif stored_token:
                return redirect(url_for('auth/login'), code=303)
                
            session['form_token'] = str(uuid.uuid4())
            
            email = sanitize_email(request.form.get('username', ''))
            password = request.form.get('password', '') 
            
            if not email or not password:
                return self._render_login_template(alert_message="Email and password are required", toast=True)

            admin = self.db_session.query(Admin).filter(Admin.email.ilike(email)).first()
            if admin and check_password_hash(admin.password_hash, password):
                login_user(admin)
                session.permanent = True 
                session['last_activity'] = 0 
                session['success_message'] = "Logged in Successfully, Admin!"
                return redirect(url_for('admin_dashboard'), code=303)
            
            user = self.db_session.query(User).filter(User.email.ilike(email)).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                session.permanent = True  
                session['last_activity'] = 0  
                session['success_message'] = f"Logged in , {email}"
                return redirect(url_for('dashboard'), code=303)
            
            return self._render_login_template(alert_message="Invalid email or password" , toast=True)
        
        session['form_token'] = str(uuid.uuid4())
        success_message = session.pop('success_message', None)
        
        return self._render_login_template(success_message=success_message, toast=bool(success_message))

    def handle_signup(self):

        if current_user.is_authenticated:
            if hasattr(current_user, 'username') and current_user.username == 'admin':
                return redirect(url_for('admin/dashboard'))
            else:
                return redirect(url_for('dashboard'))     
        if request.method == 'POST':
            form_token = request.form.get('form_token')
            stored_token = session.pop('form_token', None)
            
            if stored_token and form_token == stored_token:
                pass
            elif stored_token:
                return redirect(url_for('signup'), code=303)
                
            session['form_token'] = str(uuid.uuid4())
            
            fullname = sanitize_name(request.form.get('fullname', ''))
            email = sanitize_email(request.form.get('email', ''))
            password = request.form.get('password', '') 
            address = sanitize_address(request.form.get('address', ''))
            pincode = sanitize_pincode(request.form.get('pincode', ''))
          
            if not all([fullname, email, password, address, pincode]):
                return self._render_signup_template(alert_message="All fields are required", toast=True)

            if not email:
                return self._render_signup_template(alert_message="Please enter a valid email address", toast=True)

            existing_admin = self.db_session.query(Admin).filter(Admin.email.ilike(email)).first()
            existing_user = self.db_session.query(User).filter(User.email.ilike(email)).first()
            if existing_user or existing_admin:
                return self._render_signup_template(alert_message="Email already registered. Please use another email.", toast=True)

            if len(password) < 8:
                return self._render_signup_template(alert_message="Password must be at least 8 characters", toast=True)
                
            password_errors = self._validate_password_strength(password)
            if password_errors:
                return self._render_signup_template(alert_message=password_errors, toast=True)

            if not pincode:
                return self._render_signup_template(alert_message="Pincode must be exactly 6 digits", toast=True)

            hashed_password = generate_password_hash(password)
            new_user = User(
                FullName=fullname,
                email=email,
                password_hash=hashed_password,
                address=address,
                pincode=pincode
            )
            
            try:
                self.db_session.add(new_user)
                self.db_session.commit()
                
                session['success_message'] = "Registration successful! You can now log in."
                
                return redirect(url_for('login'), code=303)
            except Exception as e:
                self.db_session.rollback()
                return self._render_signup_template(alert_message=f"Registration failed: {str(e)}", toast=True)
        
        session['form_token'] = str(uuid.uuid4())
        
        return self._render_signup_template(toast=False)
    
    def handle_logout(self):
        logout_user()
        session['success_message'] = "Logged out successfully!"
        return redirect(url_for('login'))
    
    def _get_signup_fields(self):
        return [ {'name': 'fullname','label': 'FULL NAME','type': 'text','icon': 'user','placeholder': 'What does your ID have?'},
                 {'name': 'email','label': 'EMAIL','type': 'email','icon': 'email','placeholder': 'We promise not to spam... much 😉'},
                 {'name': 'password','label': 'PASSWORD','type': 'password','icon': 'lock','placeholder': '••••••••' },
                 {'name': 'address','label': 'ADDRESS','type': 'text','icon': 'location','placeholder': 'Where should we send your pizza? 🏠'},
                 { 'name': 'pincode','label': 'PINCODE','type': 'text','icon': 'pin','placeholder': '6 digits to find you on the map!' }
            ]
        
    def _get_lotaddition_fields(self):
        return [ 
                {'name': 'address','label': 'ADDRESS','type': 'text','icon': 'location','placeholder': '123, Main Street or something fancier'},
                {'name': 'prime location','label': 'LOCATION','type': 'text','icon': 'location','placeholder': 'What landmark is it near?'},
                {'name': 'pincode','label': 'PINCODE','type': 'text','icon': 'pin','placeholder': 'Area code magic — 6 digits'},
                {'name': 'maximum spots','label': 'CAPACITY','type': 'number','icon': 'capacity','placeholder': '1 to 150 — how many cars can you host?'},
                {'name': 'price_per_hour','label': 'PRICE PER HOUR','type': 'number','icon': 'price','placeholder': 'Charge wisely — ₹1 to ₹1000/hr'}
            ]

    def _render_signup_template(self, alert_message=None, toast=False):
        page_title = "Sign up"
        page_title1 = "Sign up to ParkEase"
        image_path = "/static/images/Log_sidebar.png"
        icon_map = {
            'email': 'svg/Email.svg',
            'lock': 'svg/Password.svg',
            'user': 'svg/User_Circle.svg',
            'location': 'svg/Address.svg',
            'pin': 'svg/Pincode.svg'
        }
        
        fields = self._get_signup_fields()
        
        return render_template('forms/form.html',
                              alert_message=alert_message,
                              toast=toast,
                              fields=fields,
                              button_text="SIGN UP",
                              button_class="login-button",
                              button_id="signup-button",
                              type='signup',
                              url = url_for('signup'),
                              icon_map=icon_map,
                              image_path=image_path,
                              Page_title=page_title,
                              Page_title1=page_title1,
                              form_token=session.get('form_token'))
                              
    def _render_login_template(self, alert_message=None, success_message=None, toast=False):
        return render_template('auth/login.html',
                              alert_message=alert_message,
                              success_message=success_message,
                              toast=toast,
                              form_token=session.get('form_token'))

    def _validate_password_strength(self, password):
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
            
        return ". ".join(errors) if errors else None



