
from flask_jwt_extended import (create_access_token, create_refresh_token, 
jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Flask, Blueprint, jsonify, request, make_response, current_app
from disasterpets.Pets.models import Pets, PetsJoin
from disasterpets import bcrypt, db, jwt
from flask_restful import Resource


class AddPetAPI(Resource):
    @jwt_required
    def post(self):
        new_pet = request.get_json()
        current_user = get_jwt_identity()
        try:
            pet = Pets(
                pet_name=new_pet.get('pet_name'),
                animal_type=new_pet.get('animal_type'),
                primary_breed=new_pet.get('primary_breed'),
                secondary_breed=new_pet.get('secondary_breed'),
                gender=new_pet.get('gender'),
                altered_status=new_pet.get('altered_status'),
                trapper_id =new_pet.get('trapper_id ')
            )
            db.session.add(pet)
            db.session.commit()


            db.session.refresh(pet)
            petjoin = PetsJoin(
                user_id = current_user,
                pet_id = pet.id
            )
            db.session.add(petjoin)
            db.session.commit()
            
            responseObject = {
                'status': 'success',
                'message': 'successfully added pet'
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404