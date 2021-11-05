from flask import render_template, request, send_file

from util import table_record_to_json, dict_keyvalue_or_default
from config import flask_app, qrcode
import qrcode
import AuthController
# from './http-common.js' import baseURL

from OrderActions import OrderActions
import io


def index():
    return render_template("index.html")


def create_order():
    AuthController.set_authorize_current_user()
    AuthController.check_update_order_allowed()
    request_json = request.get_json()
    usa_state = request_json["usa_state"]
    idbased_order_number = request_json["order_number"]
    home_office_code = request_json["home_office_code"]
    order_status = dict_keyvalue_or_default (request_json, "order_status", 1)
    order = OrderActions.create(usa_state, idbased_order_number, home_office_code, order_status)
    return table_record_to_json(order)

def get_orders():
    AuthController.set_authorize_current_user()
    orders = OrderActions.get()
    return orders


def get_order_by_uuid(uuid):
    AuthController.set_authorize_current_user()
    order_obj = OrderActions.get_order_by_uuid(uuid)
    order_dict = {"order_number": order_obj.order_number, "usa_state": order_obj.usa_state,
                  "home_office_code": order_obj.home_office_code, "uuid": order_obj.uuid}
    return order_dict


def get_order_by_order_number(order_number):
    AuthController.set_authorize_current_user()
    order_obj = OrderActions.get_order_by_order_number(order_number)
    if order_obj is None:
        return {"error": "order not found"}
    else:
        order_dict = {"order_number": order_obj.order_number, "usa_state": order_obj.usa_state,
                      "home_office_code": order_obj.home_office_code, "uuid": order_obj.uuid}
        return {"orders": [order_dict]}


# generate qr code
def get_qrcode(uuid):
    frontend_url = flask_app.config["FRONTEND_URI"]
    img = qrcode.make(frontend_url + "/api/orders/" + uuid)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return buf


# not secured as it is provided in a link where token cannot be sent
def send_file_qrcode(uuid):
    q = get_qrcode(uuid)
    return send_file(q, mimetype="image/jpeg")


def update_order(uuid):
    AuthController.set_authorize_current_user()
    order: OrderActions = OrderActions.get_order_by_uuid(uuid)
    AuthController.check_update_order_allowed(order)

    request_json =  request.get_json()
    usa_state = dict_keyvalue_or_default(request_json, "usa_state", None)
    home_office_code = dict_keyvalue_or_default(request_json, "home_office_code", None)
    order_number = dict_keyvalue_or_default(request_json, "order_number", None)
    order_status = dict_keyvalue_or_default(request_json, "order_status", None)
    updated_order = order.update_order(
        uuid, usa_state, order_number, home_office_code, order_status
    )
    order_dict = {"order_number": updated_order.order_number, "usa_state": updated_order.usa_state,
                  "home_office_code": updated_order.office_code, "uuid": updated_order.uuid}
    return order_dict

def update_order_status(uuid):
    AuthController.set_authorize_current_user()
    order: OrderActions = OrderActions.get_order_by_uuid(uuid)
    AuthController.check_update_order_allowed()

    request_json =  request.get_json()
    order_status = dict_keyvalue_or_default(request_json, "order_status", None)
    updated_order = order.update_order(
        uuid, order_status = order_status
    )