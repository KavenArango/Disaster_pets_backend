from flask_jwt_extended import (create_access_token, create_refresh_token,
jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Flask, Blueprint, jsonify, request, make_response, current_app
from disasterpets.Account.models import User
from disasterpets import bcrypt, db
import datetime
from flask_restful import Resource

class RegisterAPI(Resource):
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

                access_token = create_access_token(identity = user.id)
                refresh_token = create_refresh_token(identity = user.id)

                responseObject = {
                    'status' : 'success',
                    'message': 'successfully registered!',
                    'access_token': access_token,
                    'refresh_token': refresh_token
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


class LoginAPI(Resource):
	def post(self):
		current_user = request.get_json()
		user = User.query.filter_by(email = current_user.get('email')).first()
		if user:
			if bcrypt.check_password_hash(user.password, current_user.get("password")):
				access_token = create_access_token(identity = user.id)
				refresh_token = create_refresh_token(identity = user.id)

				if access_token:
					responseObject = {
						'status' : 'success',
						'message': 'successfully logged in!',
						'access_token': access_token,
						'refresh_token': refresh_token
					}
					return make_response(jsonify(responseObject)), 200
				else:
					responseObject = {
						'status' : 'failed',
						'message': 'something went wrong',
					}
					return make_response(jsonify(responseObject)), 200
			else:
				responseObject = {
							'status' : 'failed',
							'message': 'Email or Password Inncorect'
				}
				return make_response(jsonify(responseObject)), 500
		else:
			responseObject = {
				'status' : 'fail',
				'message': 'user does not exist'
			}
			return make_response(jsonify(responseObject)), 404

# class LogoutAPI(Resource):
#    @jwt_required
#    def post(self):
#         jti = get_raw_jwt()['jti']
#         try:
#             revoked_token = RevokedTokenModel(jti = jti)
#             revoked_token.add()
#             return {'message': 'Access token has been revoked'}
#         except Exception as e:
#             print(e)
#             return {'message': 'Something went wrong'}, 500



