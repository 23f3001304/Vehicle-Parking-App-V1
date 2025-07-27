from flask import render_template, url_for
from .getter import _get_edit_lot_fields, _get_lotaddition_fields, _get_spot_fields

def _render_editLot_template(alert_message=None, success_message=None, toast=False, lot=None, form_token=None):
        page_title = "Edit Parking Lot - ParkEase"
        page_title1 = "Edit a Parking Lot"
        image_path = "/static/images/Lot.png"
        
        icon_map = {
            'Address': 'svg/Address.svg',
            'Pincode': 'svg/Pincode.svg',
            'Capacity': 'svg/spots.svg',
            'Price': 'svg/price.svg',
            'Location': 'svg/map.svg'
        }
        
        fields = _get_edit_lot_fields(lot)
        
        from controllers.Admin.admin_utils import AdminUtils
        utils = AdminUtils(None)
        
        return render_template('forms/form.html',
                              back_link=url_for('admin_dashboard'),
                              alert_message=alert_message,
                              success_message=success_message,
                              toast=toast,
                              fields=fields,
                              button_text="Save Changes",
                              button_class="login-button",
                              button_id="editlot_button",
                              type='edit_lot',
                              url=url_for('edit_lot', lot_uuid=utils.encrypt_uuid(lot.uuid) if lot else ''),
                              image_path=image_path,
                              icon_map=icon_map,
                              Page_title=page_title,
                              Page_title1=page_title1,
                              form_token=form_token)

def _render_addLot_template(alert_message=None, success_message=None, toast=False, form_token=None):
        page_title = "Add Parking Lot - ParkEase"
        page_title1 = "Add a Parking Lot"
        image_path = "/static/images/Lot.png"
        
        icon_map = {
            'Address': 'svg/Address.svg',
            'Pincode': 'svg/Pincode.svg',
            'Capacity': 'svg/spots.svg',
            'Price': 'svg/price.svg',
            'Location': 'svg/map.svg'
        }
        
        fields = _get_lotaddition_fields()
        
        return render_template('forms/form.html',
                              back_link=url_for('admin_dashboard'),
                              alert_message=alert_message,
                              success_message=success_message,
                              toast=toast,
                              fields=fields,
                              button_text="ADD LOT",
                              button_class="login-button",
                              button_id="addlot_button",
                              type='add_lot',
                              url=url_for('add_lot'),
                              image_path=image_path,
                              icon_map=icon_map,
                              Page_title=page_title,
                              Page_title1=page_title1,
                              form_token=form_token)