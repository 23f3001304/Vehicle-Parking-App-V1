from flask import redirect, url_for, render_template, session, g
from flask_login import  current_user
from sqlalchemy.orm import joinedload
from sqlalchemy import func, and_
from controllers.base_controller import BaseController
from models import ParkingLot, Reservation, ParkingSpot, Admin
from .reservation_controller import ReservationController
from datetime import datetime, timedelta


class UserController(BaseController):
    
    def __init__(self, db_session):
        super().__init__(db_session)
        self.reservation_controller = ReservationController(db_session)
    
    def handle_dashboard(self):
        success_message = session.pop("success_message", None)
        alert_message = session.pop("alert_message", None)
        lot_raw = self.db_session.query(ParkingLot).all()
        active_reservations = (
            self.db_session.query(Reservation)
            .options(
                joinedload(Reservation.parking_spot).joinedload(ParkingSpot.parking_lot)
            )
            .filter(
                Reservation.user_id == current_user.id,
                Reservation.status == 1, 
                Reservation.end_time.is_(None)
            )
            .all()
        )
        user_reservations = []
        for res in active_reservations:
            spot = res.parking_spot
            lot = spot.parking_lot
            user_reservations.append({
                "id": res.id,
                "uuid": self.encrypt_uuid(res.uuid),
                "vehicle_number": res.vehicle_number,
                "spot_number": spot.spot_number,
                "location": lot.location,
                "start_time": res.start_time,
                "price_per_hour": lot.price_per_hour,
                "current_cost": res.current_cost,
                "end_path": url_for('end_reservation', res_uuid=self.encrypt_uuid(res.uuid))
            })
        parking_lots = []
        for lot in lot_raw:
            free_spots = lot.free_spots if lot.free_spots is not None else lot.capacity
            encrypted_uuid = self.encrypt_uuid(lot.uuid)
            if lot.free_spots > 0:  
                parking_lots.append({
                    "id": lot.id,
                    "location": lot.location,
                    "capacity": lot.capacity,
                    "free": free_spots,
                    "pincode": lot.pin_code,
                    "price_per_hour": lot.price_per_hour,
                    "book_path": f"/{encrypted_uuid}/book_lot",
                })
        
        user = current_user
        if not user:
            return redirect(url_for("login"))
            
        if isinstance(current_user, Admin):
            session["success_message"] = "Hola Admin! Here is your dashboard."
            return redirect(url_for("admin_dashboard"))
        
        template_params = {
            "parking_lots": parking_lots,
            "user": user,
            "reservations": user_reservations,
            "toast": True if alert_message or success_message else False
        }
        
        if alert_message:
            template_params["alert_message"] = alert_message
        
        if success_message:
            template_params["success_message"] = success_message
            
        return render_template("user/dashboard.html", **template_params)
    
    def handle_book_lot(self, lot_uuid):
        """Delegate to the reservation controller"""
        return self.reservation_controller.handle_book_lot(lot_uuid)
        
    def handle_end_reservation(self, res_uuid):
        """Delegate to the reservation controller"""
        return self.reservation_controller.handle_end_reservation(res_uuid)
    
    def handle_summary(self):
        """Handle user summary page"""
        from models.User import User
        
        if isinstance(current_user, Admin):
            session["success_message"] = "Hola Admin! Here is your dashboard."
            return redirect(url_for("admin_dashboard"))
        
        success_message = session.pop('success_message', None)
        alert_message = session.pop('alert_message', None)
        
        summary_data = self._get_user_summary_data()
        
        template_params = {
            'user': current_user,
            'summary_data': summary_data,
            'csp_nonce': g.get('csp_nonce', ''),
            'toast': bool(alert_message or success_message)
        }
        
        if alert_message:
            template_params['alert_message'] = alert_message
            
        if success_message:
            template_params['success_message'] = success_message
        
        return render_template('user/summary.html', **template_params)
    
    def _get_user_summary_data(self):
        """Get comprehensive summary data for the user"""
        user_id = current_user.id
        
        # Get total reservations count
        total_reservations = self.db_session.query(Reservation).filter_by(user_id=user_id).count()
        
        # Get active reservations
        active_reservations = self.db_session.query(Reservation).filter(
            Reservation.user_id == user_id,
            Reservation.status == 1,
            Reservation.end_time.is_(None)
        ).all()
        
        # Get completed reservations
        completed_reservations = self.db_session.query(Reservation).filter(
            Reservation.user_id == user_id,
            Reservation.status == 0
        ).all()
        
        # Calculate total spent
        total_spent = sum(res.current_cost or 0 for res in completed_reservations)
        current_spending = sum(res.current_cost or 0 for res in active_reservations)
        
        # Get favorite parking lots (most used) - simplified approach
        try:
            favorite_lots_raw = self.db_session.query(Reservation).options(
                joinedload(Reservation.parking_spot).joinedload(ParkingSpot.parking_lot)
            ).filter(Reservation.user_id == user_id).all()
            
            # Count usage per parking lot
            lot_usage = {}
            for res in favorite_lots_raw:
                lot_location = res.parking_spot.parking_lot.location
                lot_usage[lot_location] = lot_usage.get(lot_location, 0) + 1
            
            # Sort and take top 5
            sorted_lots = sorted(lot_usage.items(), key=lambda x: x[1], reverse=True)[:5]
            favorite_lots = [{'location': loc, 'usage_count': count} for loc, count in sorted_lots]
        except Exception as e:
            print(f"Error getting favorite lots: {e}")
            favorite_lots = []
        
        # Get recent reservations with details
        recent_reservations = self.db_session.query(Reservation).options(
            joinedload(Reservation.parking_spot).joinedload(ParkingSpot.parking_lot)
        ).filter(
            Reservation.user_id == user_id
        ).order_by(Reservation.id.desc()).limit(10).all()
        
        # Format recent reservations for display
        recent_activities = []
        for res in recent_reservations:
            spot = res.parking_spot
            lot = spot.parking_lot
            recent_activities.append({
                'id': res.id,
                'location': lot.location,
                'spot_number': spot.spot_number,
                'vehicle_number': res.vehicle_number,
                'start_time': res.start_time,
                'end_time': res.end_time,
                'status': 'Active' if res.status == 1 and res.end_time is None else 'Completed',
                'cost': res.current_cost or 0,
                'icon': 'fa-car' if res.status == 1 and res.end_time is None else 'fa-check-circle'
            })
        
        # Get parking statistics
        parking_stats = {
            'most_used_location': favorite_lots[0]['location'] if favorite_lots else 'N/A',
            'most_used_count': favorite_lots[0]['usage_count'] if favorite_lots else 0,
            'average_cost_per_session': round(total_spent / len(completed_reservations), 2) if completed_reservations else 0,
            'total_parking_sessions': total_reservations
        }
        
        # Prepare chart data for spending over time
        spending_chart_data = {
            'labels': [lot['location'] for lot in favorite_lots],
            'data': [lot['usage_count'] for lot in favorite_lots]
        }
        
        return {
            'total_reservations': total_reservations,
            'active_reservations_count': len(active_reservations),
            'completed_reservations_count': len(completed_reservations),
            'total_spent': total_spent,
            'current_spending': current_spending,
            'favorite_lots': [{'location': lot['location'], 'count': lot['usage_count']} for lot in favorite_lots],
            'recent_activities': recent_activities,
            'parking_stats': parking_stats,
            'spending_chart_data': spending_chart_data,
            'active_reservations': [{
                'id': res.id,
                'location': res.parking_spot.parking_lot.location,
                'spot_number': res.parking_spot.spot_number,
                'vehicle_number': res.vehicle_number,
                'start_time': res.start_time,
                'current_cost': res.current_cost or 0,
                'price_per_hour': res.parking_spot.parking_lot.price_per_hour
            } for res in active_reservations]
        }
