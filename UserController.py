from flask import request

from AuthController import set_authorize_current_user, check_is_admin
from UserActions import UserActions
from models import UserParams


def create_user():
    print("Creating")
    set_authorize_current_user()
    check_is_admin()
    request_json = request.get_json()
    userParams = UserParams()
    userParams.username = request_json["username"]
    userParams.password = request_json["password"]
    userParams.can_create_update_delete_orders = request_json[
        "can_create_update_delete_orders"
    ]
    userParams.office_code = request_json[
        "office_code"
    ]
    userParams.can_update_password_for = request_json["can_update_password_for"]
    userParams.can_update_status_for = request_json["can_update_status_for"]
    userParams.is_admin = request_json["is_admin"]
    new_user = UserActions.create(userParams)
    return new_user, 201
