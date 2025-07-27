"""
Admin Routes
Handles all admin-related routes and endpoints
"""
from flask import redirect, url_for, session
from flask_login import login_required, current_user
from models import Admin


def register_admin_routes(app, admin_controller):
    
    def admin_required(f):
        def decorated_function(*args, **kwargs):
            if not isinstance(current_user, Admin):
                session["alert_message"] = "You are not authorized to access that page."
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    
    @app.route('/admin/dashboard')
    @login_required
    @admin_required
    def admin_dashboard():
        return admin_controller.handle_admin_dashboard()

    @app.route('/admin/add_lot', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def add_lot():
        return admin_controller.handle_lot_addition()

    @app.route('/admin/lot/<path:lot_uuid>/edit', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def edit_lot(lot_uuid):
        return admin_controller.handle_lot_edit(lot_uuid)

    @app.route('/admin/lot/<path:lot_uuid>/spots')
    @login_required
    @admin_required
    def view_spots(lot_uuid):
        return admin_controller.handle_view_spots(lot_uuid)

    @app.route('/admin/lot/<path:lot_uuid>/delete')
    @login_required
    @admin_required
    def delete_lot(lot_uuid):
        return admin_controller.handle_delete_lot(lot_uuid)

    @app.route('/admin/<path:spot_uuid>/view_spots', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def view_spot(spot_uuid):
        return admin_controller.handle_view_spot(spot_uuid)

    @app.route('/admin/reservation/<path:spot_uuid>/')
    @login_required
    @admin_required
    def view_reservation(spot_uuid):
        return admin_controller.handle_view_reservation(spot_uuid)

    @app.route('/admin/users')
    @login_required
    @admin_required
    def view_users():
        return admin_controller.handle_view_users()

    @app.route('/admin/summary')
    @login_required
    @admin_required
    def admin_summary():
        return admin_controller.handle_summary()

    @app.route('/admin/search')
    @login_required
    @admin_required
    def admin_search():
        return admin_controller.handle_search()
