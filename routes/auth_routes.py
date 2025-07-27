"""
Authentication Routes
Handles login, signup, logout, and main routing
"""
from flask import redirect, url_for, session
from flask_login import current_user, login_required
from models import Admin


def register_auth_routes(app, auth_controller, user_controller):
    
    @app.route('/')
    def home():
        if current_user.is_authenticated:
            if isinstance(current_user, Admin):
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return auth_controller.handle_login()

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        return auth_controller.handle_signup()

    @app.route('/logout')
    @login_required  
    def logout():
        return auth_controller.handle_logout()

    @app.route('/dashboard')
    @login_required
    def dashboard():
        if isinstance(current_user, Admin):
            session["success_message"] = "Hola Admin! Here is your dashboard."
            return redirect(url_for("admin_dashboard"))
        return user_controller.handle_dashboard()
