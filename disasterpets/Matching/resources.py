from flask_jwt_extended import (create_access_token, create_refresh_token, 
jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Flask, Blueprint, jsonify, request, make_response, current_app
from disasterpets.Pets.models import Pets, PetsJoin
from disasterpets import bcrypt, db, jwt
from flask_restful import Resource
from disasterpets.Pets.schema import PetsSchema, BreedSchema, GenderSchema, PetStatusSchema, AnimalSchema, AlteredSchema
from disasterpets.Pets.models import Pets, PetsJoin, Breeds, Gender, AlteredStatus, PetStatus, Animals
from disasterpets.Pictures.models import PetImageJoin
from disasterpets.Pictures.schema import PetsImageJoinSchema
from disasterpets.Pets.resourceFunctions import collectAllUniqueFeature


class PetMatchAPI(Resource):
    def get(self):
        searchingfor = request.get_json()
        #pets_schema = PetsSchema(many=True)
        imagejoin_schema = PetsImageJoinSchema(many = True)
        breeds_schema = BreedSchema(many=True)
        genders_schema = GenderSchema(many = True)
        petstat_schema = PetStatusSchema(many =True)
        animals_schema = AnimalSchema(many=True)
        altered_schema = AlteredSchema(many=True)

        try:
            if searchingfor == None:
                searchingfor = PetImageJoin.query.all()
                jresults = imagejoin_schema.dump(searchingfor)
                allbreeds = Breeds.query.all()
                breedresult = breeds_schema.dump(allbreeds)
                allgenders = Gender.query.all()
                genderesults = genders_schema.dump(allgenders)
                allpetstat = PetStatus.query.all()
                statusresults = petstat_schema.dump(allpetstat)
                allanimals = Animals.query.all()
                animalresults = animals_schema.dump(allanimals)
                altered = AlteredStatus.query.all()
                alteredresults = altered_schema.dump(altered)

            
                responseObject = {
                    'status' : 'success',
                    'message': 'successfully Pulled!',
                    'pets': jresults,
                    'breeds': breedresult,
                    'genders': genderesults,
                    'animal': animalresults,
                    'status': statusresults,
                    'altered': alteredresults,
                    'UniqueFeatures': collectAllUniqueFeature()
                }
                return make_response(jsonify(responseObject)), 201
                
        except Exception as e:
            print(e)
            responseObject = {
                'status' : 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404