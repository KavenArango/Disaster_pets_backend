from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Flask, Blueprint, json, jsonify, request, make_response, current_app
from disasterpets.Account.models import User
from disasterpets.Account.Schema import UserSchema
from disasterpets.Pets.models import PetsJoin
from disasterpets.Pets.schema import PetsJoinSchema
from disasterpets.Pictures.models import PetImageJoin
from disasterpets.Pictures.schema import PetsImageJoinSchema
from disasterpets import bcrypt, db, jwt
import datetime
from flask_restful import Resource
import json as simplejson


class RegisterAPI(Resource):
    def post(self):
        new_user = request.get_json()

        user = User.query.filter_by(email=new_user.get('email')).first()
        if not user:
            try:
                user = User(
                    fname=new_user.get('fname'),
                    lname=new_user.get('lname'),
                    email=new_user.get('email'),
                    password=new_user.get('password'),
                    phone=new_user.get('phone'),
                    phone2=new_user.get('phone2'),
                    role_id=new_user.get('role_id'),
                    social=new_user.get('social')
                )
                db.session.add(user)
                db.session.commit()
                access_token = user.encode_auth_token(user.id,user.role_id)
                string_token = access_token.decode("utf-8")
                #access_token = create_access_token(identity = user.id)
                refresh_token = create_refresh_token(identity = user.id)

                responseObject = {
                    'status': 'success',
                    'message': 'successfully registered!',
                    'access_token': string_token,
                    'refresh_token': refresh_token
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'failed',
                    'message': 'something went wrong try again'
                }
                return make_response(jsonify(responseObject)), 404
        else:
            responseObject = {
                'status': 'failed',
                'message': 'User already exists'
            }
            return make_response(jsonify(responseObject)), 202


class LoginAPI(Resource):
    def post(self):
        current_user = request.get_json()
        user = User.query.filter_by(email = current_user.get('email')).first()
        if user:
            if bcrypt.check_password_hash(user.password, current_user.get("password")):
                access_token = user.encode_auth_token(user.id, user.role_id)
                string_token = access_token.decode("utf-8")
				#access_token = create_access_token(identity = user.id)
                refresh_token = create_refresh_token(identity = user.id)
                if access_token:
                    responseObject = {
						'status' : 'success',
						'message': 'successfully logged in!',
						'access_token': string_token,
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

class DashboardAPI(Resource):
    def get(self):
        current = request.headers.get('Authorization')
        if current:
            current = current.split(" ")[1]
        else:
            current = ''
        if current:
            resp = User.decode_auth_token(current)
        imagejoin_schema = PetsImageJoinSchema(many = True)
        petsjoin_schema = PetsJoinSchema(many = True)

        try:
            gettingpetid = PetsJoin.query.filter(PetsJoin.user_id == resp['identity']).with_entities(PetsJoin.pet_id).all()
            m_pets = petsjoin_schema.dump(gettingpetid)
            pets = []
            for x in m_pets:
                petinfo = PetImageJoin.query.filter(PetImageJoin.pet_id == x['pet_id']).all()
                jresults = imagejoin_schema.dump(petinfo)
                pets.append(jresults)
        
            responseObject = {
                'status' : 'success',
                'message': 'successfully Pulled!',
                'pets': pets,
            }
            return make_response(jsonify(responseObject)), 201
                
        except Exception as e:
            print(e)
            responseObject = {
                'status' : 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404





def collectAllUsers():
    userSchema = UserSchema(many = True)
    allUsers = User.query.all()
    userresults = userSchema.dump(allUsers)
    responseObject = {
        'status': 'sucess',
        'allUsers': userresults,
        'message': 'all users returned'
        }
    return responseObject




def collectAllUsers():
    userSchema = UserSchema(many = True)
    allUsers = User.query.all()
    userresults = userSchema.dump(allUsers)
    responseObject = {
        'status': 'sucess',
        'Users': userresults,
        'message': 'all users returned'
        }
    return responseObject


def collectOneUser(requestedData):
    oneUsers = User.query.filter(requestedData['id'] == User.id)
    userSchema = UserSchema(many = True)
    userresults = userSchema.dump(oneUsers)
    responseObject = {
        'status': 'sucess',
        'Users': userresults,
        'message': 'user has been returned'
        }
    return responseObject


def editUser(requestedData):
    oneUser = User.query.filter(requestedData['id'] == User.id).first()
    oneUser.fname = requestedData['fname']
    oneUser.lname = requestedData['lname']
    oneUser.email = requestedData['email']
    oneUser.phone = requestedData['phone']
    oneUser.phone2 = requestedData['phone2']
    oneUser.role_id = requestedData['role_id']
    # oneUser.social = requestedData['social']
    db.session.commit()




class ManageUserAPI(Resource):
    # @jwt_required
    def get(self):  # taking from client giving to db
        try:
            requestedData = request.get_json()
            data = collectOneUser(requestedData)
            if data == []:
                responseObject = {
                    'status': 'error',
                    'message': 'No users found'
                    }
                return make_response(jsonify(responseObject)), 500
            
            else:
                
                editUser(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'user updated'
                    }
                
                return make_response(jsonify(responseObject)), 201
            
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404

    def post(self):  # asking from db to client
        try:
            requestedData = request.get_json()
            responseObject = {}
            if requestedData.get('id') == 'null': # giving back all the users
                
                found, responseObject = collectAllUsers()
                
            
            elif requestedData  != 'null': # asking for a specific user
                
                responseObject = collectOneUser(requestedData)
                
            
            if responseObject['Users'] == []:
                responseObject = {
                    'status': 'error',
                    'message': 'No user found'
                }
                return make_response(jsonify(responseObject)), 500
            
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404




