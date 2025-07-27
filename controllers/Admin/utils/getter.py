def _get_lotaddition_fields():
        return [ 
                {'name': 'prime location','label': 'LOCATION','type': 'text','icon': 'Location','placeholder': 'What landmark is it near?'},
                {'name': 'address','label': 'ADDRESS','type': 'text','icon': 'Address','placeholder': '123, Main Street - keep it short'},
                {'name': 'pincode','label': 'PINCODE','type': 'text','icon': 'Pincode','placeholder': '6 digits [only one lot per pincode]'},
                {'name': 'maximum spots','label': 'CAPACITY','type': 'number','icon': 'Capacity','placeholder': '1 to 50 - how many cars can you host?'},
                {'name': 'price_per_hour','label': 'PRICE PER HOUR','type': 'number','icon': 'Price','placeholder': 'Charge wisely - ₹1 to ₹1000/hr'}
            ]
            
def _get_edit_lot_fields(lot):
        return [ 
                {'name': 'prime location','label': 'LOCATION','type': 'text','icon': 'Location','placeholder': 'What landmark is it near?', 'value': lot.location if lot else ''},
                {'name': 'address','label': 'ADDRESS','type': 'text','icon': 'Address','placeholder': '123, Main Street - keep it short', 'value': lot.address if lot else ''},
                {'name': 'pincode','label': 'PINCODE','type': 'text','icon': 'Pincode','placeholder': '6 digits [only one lot per pincode]', 'value': lot.pin_code if lot else ''},
                {'name': 'maximum spots','label': 'CAPACITY','type': 'number','icon': 'Capacity','placeholder': '1 to 50 - how many cars can you host?' , 'value': lot.capacity if lot else ''},
                {'name': 'price_per_hour','label': 'PRICE PER HOUR','type': 'number','icon': 'Price','placeholder': 'Charge wisely - ₹1 to ₹1000/hr' , 'value': lot.price_per_hour if lot else ''}
            ]
def _get_spot_fields(spot):
        return [ 
                {'name': 'lot_id','label': 'Lot Id','type': 'text','icon': 'id','placeholder': 'What landmark is it near?', 'value': spot.parking_lot_id if spot else '' , 'disabled': True},
                {'name': 'spot_id','label': 'Spot Nubmer','type': 'text','icon': 'spot','placeholder': '123, Main Street - keep it short', 'value':spot.spot_number if spot else ' ', 'disabled': True},
                {'name': 'status','label': 'Status','type': 'text','icon': 'status','placeholder': '6 digits [only one lot per pincode]', 'value': 'Available' if spot.status == 0 else 'Occupied' , 'disabled': True},
            ]    