from flask import Flask, Blueprint, jsonify, request, make_response, current_app
from disasterpets.Account.models import User
from disasterpets import db, bcrypt
from flask.views import MethodView
import jwt 
import datetime
from disasterpets.Account.resources import LoginAPI, RegisterAPI# LogoutAPI

account = Blueprint('account', __name__)

registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
# logout_view = LogoutAPI.as_view('logout_api')

account.add_url_rule(
    '/register',
    view_func=registration_view,
    methods=['POST']
)

account.add_url_rule(
    '/login',
    view_func= login_view,
    methods=['POST']
)

# account.add_url_rule(
#     '/logout/access',
#     view_func= logout_view,
#     methods=['POST']
# )
