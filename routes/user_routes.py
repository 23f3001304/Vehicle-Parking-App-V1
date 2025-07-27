"""
User Routes
Handles all user-related routes and endpoints
"""
from flask import redirect, url_for, session
from flask_login import login_required, current_user
from models import User


def register_user_routes(app, user_controller):    
    def user_required(f):
        def decorated_function(*args, **kwargs):
            if not isinstance(current_user, User):
                session["alert_message"] = "You are not authorized to access that page."
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function

    @app.route('/<path:lot_uuid>/book_lot', methods=['GET', 'POST'])
    @login_required
    @user_required
    def book_spot(lot_uuid):
        """Book a parking spot in a lot"""
        return user_controller.handle_book_lot(lot_uuid)

    @app.route('/reservation/<path:res_uuid>/end')
    @login_required
    @user_required
    def end_reservation(res_uuid):
        """End an active reservation"""
        return user_controller.handle_end_reservation(res_uuid)

    @app.route('/user/summary')
    @login_required
    @user_required
    def user_summary():
        """User analytics and summary"""
        return user_controller.handle_summary()
