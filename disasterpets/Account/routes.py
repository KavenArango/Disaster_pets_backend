from flask import Flask, Blueprint, jsonify, request, make_response, current_app
from disasterpets.Account.models import User
from disasterpets import db, bcrypt
from flask.views import MethodView
import jwt 
import datetime

account = Blueprint('account', __name__)

#API methods


class RegisterAPI(MethodView):
    def post(self):
        new_user = request.get_json()

        user = User.query.filter_by(email = new_user.get('email')).first()
        if not user:
            try:
                user = User(
                    fname = new_user.get('fname'),
                    lname = new_user.get('lname'),
                    email = new_user.get('email'),
                    password = new_user.get('password'),
                    phone = new_user.get('phone'),
                    phone2 = new_user.get('phone2'),
                    role_id = new_user.get('role_id')
                )
                db.session.add(user)
                db.session.commit()

                auth_token = user.encode_auth_token(user.id)
                print(auth_token)
                responseObject = {
                    'status' : 'success',
                    'message': 'successfully registered!',
                    'auth_token' : auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print(e)
                responseObject = {
                    'status' : 'failed',
                    'message': 'something went wrong try again'
                }
                return make_response(jsonify(responseObject)), 404
        else:
            responseObject = {
                    'status' : 'failed',
                    'message': 'User already exists'
                }
            return make_response(jsonify(responseObject)), 202


class LoginAPI(MethodView):
    def post(self):
        current_user = request.get_json()
        try:
            user = User.query.filter_by(email = current_user.get('email')).first()
            if user and bcrypt.check_password_hash(user.password, current_user.get("password")):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'status' : 'success',
                        'message': 'successfully logged in!',
                        'auth_token' : auth_token.decode()
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'status' : 'fail',
                        'message': 'user does not exist'
                    }
                    return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                        'status' : 'failed',
                        'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 500



registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')

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
