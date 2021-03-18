from flask import Flask, Blueprint, jsonify, request, make_response, current_app
from disasterpets.Account.models import User
from disasterpets import db, bcrypt, mail, url
from flask.views import MethodView
import jwt
import datetime

from disasterpets.Account.resources import (
    LoginAPI,
    RegisterAPI,
    ManageUserAPI,
    DashboardAPI,
    ManageRoleAPI,
	ForgotPasswordAPI,
	ResetPasswordAPI
)  # LogoutAPI, DashboardAPI


account = Blueprint("account", __name__)

registration_view = RegisterAPI.as_view("register_api")
login_view = LoginAPI.as_view("login_api")
dashboard_view = DashboardAPI.as_view("dashboard_api")
manageruser_view = ManageUserAPI.as_view("manageuser_api")
managerole_view = ManageRoleAPI.as_view('managerole_api')
forgotpassword_view = ForgotPasswordAPI.as_view('forgotpassword_api')
resetpassword_view = ResetPasswordAPI.as_view('resetpassword_api')

account.add_url_rule(
    "/register",
    view_func=registration_view,
    methods=["POST"]
    )

account.add_url_rule(
    "/login", 
    view_func=login_view, 
    methods=["POST"]
    )

account.add_url_rule(
    "/dashboard", 
    view_func=dashboard_view, 
    methods=["GET"]
    )

account.add_url_rule(
    "/manageuser", 
    view_func=manageruser_view, 
    methods=["PATCH", "POST"]
)


account.add_url_rule(
    '/managerole',
    view_func= managerole_view,
    methods=['POST', 'PATCH', 'GET']
)

account.add_url_rule(
    '/forgotpassword',
    view_func= forgotpassword_view,
    methods=['POST']
)

account.add_url_rule(
    '/resetpassword',
    view_func= resetpassword_view,
    methods=['POST']
)
# account.add_url_rule(
#     '/logout/access',
#     view_func= logout_view,
#     methods=['POST']
# )
