from flask import render_template, url_for, redirect, session, g, request
from flask_login import current_user
from controllers.base_controller import BaseController

from .lot import LotController
from .spot import SpotController
from .admin_utils import AdminUtils
from models import User, ParkingSpot, Reservation,  ParkingLot, Admin

from sqlalchemy import or_, and_
class AdminController(BaseController):    
    def __init__(self, db_session):
        super().__init__(db_session)
        self.utils = AdminUtils(db_session)
        self.lot_controller = LotController(db_session,self.utils)
        self.spot_controller = SpotController(db_session,self.utils)
        
    def handle_admin_dashboard(self): 
        if not isinstance(current_user, Admin):
            session["alert_message"] = "You are not authorized to access that page."
            return redirect(url_for('dashboard'))
            
        success_message = session.pop('success_message', None)
        alert_message = session.pop('alert_message', None)
        
        parking_lots_raw = self.db_session.query(ParkingLot).filter_by(admin_id=current_user.id).all()
        parking_lots = []
        
        for lot in parking_lots_raw:
            free_spots = lot.free_spots if lot.free_spots is not None else lot.capacity
            encrypted_uuid = self.encrypt_uuid(lot.uuid)
            parking_lots.append({
                'id': lot.id,
                'uuid': lot.uuid,
                'location': lot.location,
                'capacity': lot.capacity,
                'free': free_spots,
                'pincode': lot.pin_code,
                'price_per_hour': lot.price_per_hour,
                'edit_path': url_for('edit_lot', lot_uuid=encrypted_uuid),
                'view_path': url_for('view_spots', lot_uuid=encrypted_uuid),
                'delete_path': url_for('delete_lot', lot_uuid=encrypted_uuid)
            })
            
        template_params = {
            'admin_email': current_user.email,
            'parking_lots': parking_lots,
            'csp_nonce': g.get('csp_nonce', ''),
            'toast': bool(alert_message or success_message)
        }
        
        if alert_message:
            template_params['alert_message'] = alert_message
            
        if success_message:
            template_params['success_message'] = success_message
        
        return render_template('admin/dashboard.html', **template_params)
    
    def handle_lot_addition(self):
        return self.lot_controller.handle_lot_addition()
        
    def handle_lot_edit(self, encrypted_uuid):
        return self.lot_controller.handle_lot_edit(encrypted_uuid)
        
    def handle_delete_lot(self, encrypted_uuid):
        return self.lot_controller.handle_delete_lot(encrypted_uuid)
        
    def handle_view_spots(self, encrypted_uuid):
        return self.spot_controller.handle_view_spots(encrypted_uuid)
        
    def handle_view_spot(self, spot_uuid):
        return self.spot_controller.handle_view_spot(spot_uuid)
    
    def handle_view_reservation(self, reservation_uuid):
        return self.spot_controller.handle_view_reservation(reservation_uuid)
    
    def handle_view_users(self):
        """Handle viewing all users"""
        if not isinstance(current_user, Admin):
            session["alert_message"] = "You are not authorized to access that page."
            return redirect(url_for('dashboard'))
        
        users = self.db_session.query(User).all()
        return render_template('admin/users.html', users=users)
    
    def handle_search(self):
        """Handle universal search for admin"""
        if not isinstance(current_user, Admin):
            session["alert_message"] = "You are not authorized to access that page."
            return redirect(url_for('dashboard'))
        
        search_query = request.args.get('q', '').strip()
        search_results = {}
        
        if search_query:
            search_results = self._perform_search(search_query)
        
        template_params = {
            'admin_email': current_user.email,
            'search_query': search_query,
            'search_results': search_results,
            'csp_nonce': g.get('csp_nonce', ''),
            'toast': False
        }
        
        return render_template('admin/search.html', **template_params)
    
    def handle_summary(self):
        """Handle admin summary page"""
        if not isinstance(current_user, Admin):
            session["alert_message"] = "You are not authorized to access that page."
            return redirect(url_for('dashboard'))
        
        success_message = session.pop('success_message', None)
        alert_message = session.pop('alert_message', None)
        
        summary_data = self._get_summary_data()
        
        template_params = {
            'admin_email': current_user.email,
            'summary_data': summary_data,
            'csp_nonce': g.get('csp_nonce', ''),
            'toast': bool(alert_message or success_message)
        }
        
        if alert_message:
            template_params['alert_message'] = alert_message
            
        if success_message:
            template_params['success_message'] = success_message
        
        return render_template('admin/summary.html', **template_params)
    
    def _perform_search(self, query):
        results = {
            'parking_lots': [],
            'users': [],
            'reservations': [],
            'parking_spots': []
        }
        
        lots = self.db_session.query(ParkingLot).filter(
            and_(
                ParkingLot.admin_id == current_user.id,
                or_(
                    ParkingLot.location.ilike(f'%{query}%'),
                    ParkingLot.pin_code.ilike(f'%{query}%')
                )
            )
        ).all()
        
        for lot in lots:
            encrypted_uuid = self.encrypt_uuid(lot.uuid)
            results['parking_lots'].append({
                'id': lot.id,
                'location': lot.location,
                'capacity': lot.capacity,
                'free_spots': lot.free_spots or 0,
                'pincode': lot.pin_code,
                'price_per_hour': lot.price_per_hour,
                'revenue': lot.revenue_generated or 0,
                'view_url': url_for('view_spots', lot_uuid=encrypted_uuid),
                'edit_url': url_for('edit_lot', lot_uuid=encrypted_uuid)
            })
        
        users = self.db_session.query(User).filter(
            or_(
                User.FullName.ilike(f'%{query}%'),
                User.email.ilike(f'%{query}%'),
                User.address.ilike(f'%{query}%')
            )
        ).all()
        
        for user in users:
            reservation_count = self.db_session.query(Reservation).join(ParkingSpot).join(ParkingLot).filter(
                ParkingLot.admin_id == current_user.id,
                Reservation.user_id == user.id
            ).count()
            
            results['users'].append({
                'id': user.id,
                'name': user.FullName,
                'email': user.email,
                'address': user.address,
                'reservation_count': reservation_count
            })
        
        reservations = self.db_session.query(Reservation).join(ParkingSpot).join(ParkingLot).join(User).filter(
            and_(
                ParkingLot.admin_id == current_user.id,
                or_(
                    User.FullName.ilike(f'%{query}%'),
                    User.email.ilike(f'%{query}%'),
                    ParkingLot.location.ilike(f'%{query}%'),
                    ParkingSpot.spot_number.ilike(f'%{query}%')
                )
            )
        ).limit(20).all()
        
        for reservation in reservations:
            results['reservations'].append({
                'id': reservation.id,
                'user_name': reservation.user.FullName,
                'user_email': reservation.user.email,
                'lot_location': reservation.parking_spot.parking_lot.location,
                'spot_number': reservation.parking_spot.spot_number,
                'start_time': reservation.start_time,
                'end_time': reservation.end_time,
                'status': 'Active' if reservation.status == 1 else 'Completed',
                'total_cost': reservation.current_cost or 0
            })
        
        spots = self.db_session.query(ParkingSpot).join(ParkingLot).filter(
            and_(
                ParkingLot.admin_id == current_user.id,
                or_(
                    ParkingSpot.spot_number.ilike(f'%{query}%'),
                    ParkingLot.location.ilike(f'%{query}%')
                )
            )
        ).limit(20).all()
        
        for spot in spots:
            is_occupied = self.db_session.query(Reservation).filter(
                Reservation.parking_spot_id == spot.id,
                Reservation.status == 1,
                Reservation.end_time.is_(None)
            ).first() is not None
            
            current_reservation = self.db_session.query(Reservation).filter(
                Reservation.parking_spot_id == spot.id,
                Reservation.status == 1,
                Reservation.end_time.is_(None)
            ).first()
            current_cost = current_reservation.current_cost if current_reservation else 0
            
            results['parking_spots'].append({
                'id': spot.id,
                'spot_number': spot.spot_number,
                'lot_location': spot.parking_lot.location,
                'is_occupied': is_occupied,
                'current_cost': current_cost,
                'view_url': url_for('view_spot', spot_uuid=self.encrypt_uuid(spot.uuid))
            })
        
        return results

    def _get_summary_data(self):
        total_lots = self.db_session.query(ParkingLot).filter_by(admin_id=current_user.id).count()
        total_spots = self.db_session.query(ParkingSpot).join(ParkingLot).filter(ParkingLot.admin_id == current_user.id).count()
        total_users = self.db_session.query(User).count()
        total_reservations = self.db_session.query(Reservation).join(ParkingSpot).join(ParkingLot).filter(ParkingLot.admin_id == current_user.id).count()
        

        lots = self.db_session.query(ParkingLot).filter_by(admin_id=current_user.id).all()
        available_spots = sum(lot.free_spots or 0 for lot in lots)
        
    
        active_reservations = self.db_session.query(Reservation).join(ParkingSpot).join(ParkingLot).filter(
            ParkingLot.admin_id == current_user.id,
            Reservation.status == 1,
            Reservation.end_time.is_(None)
        ).count()
        
    
        total_revenue = sum(lot.revenue_generated or 0 for lot in lots)    
        top_lots = []
        max_revenue = 0
        for lot in lots:
            revenue = lot.revenue_generated or 0
            if revenue > max_revenue:
                max_revenue = revenue
            top_lots.append({
                'location': lot.location,
                'revenue': revenue
            })
        
        top_lots = sorted(top_lots, key=lambda x: x['revenue'], reverse=True)[:5]
        
        occupied_spots = total_spots - available_spots
        overall_occupancy = round((occupied_spots / total_spots * 100) if total_spots > 0 else 0, 1)
        
        recent_activities = [
            {
                'icon': 'fa-car',
                'text': f'{active_reservations} active reservations',
                'time': 'Current'
            },
            {
                'icon': 'fa-building',
                'text': f'{total_lots} parking lots managed',
                'time': 'Total'
            },
            {
                'icon': 'fa-users',
                'text': f'{total_users} registered users',
                'time': 'Total'
            },
            {
                'icon': 'fa-money-bill-wave',
                'text': f'₹{total_revenue:.2f} revenue generated',
                'time': 'Total'
            }
        ]
        
        occupancy_chart_data = {
            'labels': [lot.location for lot in lots],
            'data': [round((lot.capacity - (lot.free_spots or 0)) / lot.capacity * 100, 1) if lot.capacity > 0 else 0 for lot in lots]
        }
        
        revenue_chart_data = {
            'labels': [lot.location for lot in lots],
            'data': [lot.revenue_generated or 0 for lot in lots]
        }
        
        return {
            'total_lots': total_lots,
            'total_spots': total_spots,
            'total_users': total_users,
            'total_reservations': total_reservations,
            'available_spots': available_spots,
            'active_reservations': active_reservations,
            'total_revenue': total_revenue,
            'top_lots': top_lots,
            'max_revenue': max_revenue,
            'overall_occupancy': overall_occupancy,
            'recent_activities': recent_activities,
            'occupancy_chart_data': occupancy_chart_data,
            'revenue_chart_data': revenue_chart_data
        }


