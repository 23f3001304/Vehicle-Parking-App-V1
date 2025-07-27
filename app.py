from flask import Flask, redirect, url_for, request, session
from flask_login import LoginManager, current_user, login_required
import os
from datetime import timedelta, timezone, datetime
import uuid
from werkzeug.security import generate_password_hash
from db import  db_session, init_db, shutdown_session
from models import User, Admin
from controllers import AuthController, AdminController, UserController


from routes.admin_routes import register_admin_routes
from routes.auth_routes import register_auth_routes
from routes.user_routes import register_user_routes

static_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, 
           static_folder=static_folder_path,
           static_url_path='/static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'I_Love_TALKING')  
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///parkease.db')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  
app.config['SESSION_COOKIE_NAME'] = 'parkease_session'  
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
auth_controller = AuthController(db_session)
admin_controller = AdminController(db_session)
user_controller = UserController(db_session)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

init_db()

def create_admin_user():
    admin = db_session.query(Admin).filter(Admin.email.ilike('admin@parkease.ac.in')).first()
    if not admin:
        admin_password = os.environ.get('ADMIN_PASSWORD', 'Park@ezy')
        admin_password_hash = generate_password_hash(admin_password)
        admin = Admin(
            id = str(uuid.uuid1()),
            username='admin',
            password_hash=admin_password_hash,
            email='admin@parkease.ac.in'  
        )
        db_session.add(admin)
        try:
            db_session.commit()
            print("Initial admin user created")
        except Exception as e:
            db_session.rollback()
            print(f"Failed to create admin user: {e}")

create_admin_user()

from scheduler import start_scheduler
scheduler = start_scheduler()

# Register all routes
register_admin_routes(app, admin_controller)
register_auth_routes(app, auth_controller, user_controller)
register_user_routes(app, user_controller)

@login_manager.user_loader
def load_user(user_id):
    admin = db_session.query(Admin).get(str(user_id))
    if admin:
        return admin
    user = db_session.query(User).get(int(user_id))
    if user:
        return user
    return None

@app.after_request
def add_no_cache(response):
    if request.method == 'POST' or request.path.startswith('/login') or request.path.startswith('/signup'):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
    return response

@app.teardown_appcontext
def shutdown_session_handler(exception=None):
    shutdown_session()

@app.before_request
def before_request():
    from datetime import datetime
    session.permanent = True 
    if current_user.is_authenticated:
        current_time = datetime.now(timezone.utc).timestamp()
        if 'last_activity' in session:
            last_activity = session['last_activity']
            inactive_duration = current_time - last_activity            
            max_inactive_seconds = app.config['PERMANENT_SESSION_LIFETIME'].total_seconds() - 60
            if inactive_duration > max_inactive_seconds:
                session.permanent = True 
        session['last_activity'] = current_time
if __name__ == '__main__':
    os.makedirs(static_folder_path, exist_ok=True)
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
