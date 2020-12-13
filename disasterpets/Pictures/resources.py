from flask_jwt_extended import (create_access_token, create_refresh_token, 
jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Flask, jsonify, request, make_response, current_app
import json 
from disasterpets import bcrypt, db, jwt
from flask_restful import Resource
from disasterpets.Pets.schema import PetsSchema, BreedSchema, GenderSchema
from disasterpets.Pets.models import Pets, PetsJoin, Breeds, Gender, AlteredStatus, PetStatus, Animals


class PetGalleryAPI(Resource):
    def get(self):
        searchingfor = request.get_json()
        pets_schema = PetsSchema(many=True)
        breeds_schema = BreedSchema(many=True)
        genders_schema = GenderSchema(many = True)

        try:
            if searchingfor == None:
                searchingfor = Pets.query.all()
                jresults = pets_schema.dump(searchingfor)
                allbreeds = Breeds.query.all()
                breedresult = breeds_schema.dump(allbreeds)
                allgenders = Gender.query.all()
                genderesults = genders_schema.dump(allgenders)

            
                responseObject = {
                    'status' : 'success',
                    'message': 'successfully Pulled!',
                    'pets': jresults,
                    'breeds': breedresult,
                    'genders': genderesults
                }
                return make_response(jsonify(responseObject)), 201
                
            responseObject = {
                    'status' : 'failure',
                    'message': 'No query done',
                    
                }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            print(e)
            responseObject = {
                'status' : 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404


        