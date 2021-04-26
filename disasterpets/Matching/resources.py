from flask_jwt_extended import (create_access_token, create_refresh_token, 
jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Flask, Blueprint, jsonify, request, make_response, current_app
from disasterpets.Pets.models import Pets, PetsJoin
from disasterpets import bcrypt, db, jwt
from flask_restful import Resource

from disasterpets.Matching.models import PotentialMatchJoin
from disasterpets.Matching.schema import PotentialMatchJoinSchema

from disasterpets.Pets.resourceFunctions import collectAllPets, collectAllFeaturesForOnePet

from disasterpets.Pets.schema import (
    PetsSchema,
    BreedSchema,
    GenderSchema,
    PetStatusSchema,
    AnimalSchema,
    AlteredSchema,
    UniqueFeaturesJoinSchema,
    UniqueFeatureNameSchema,
    UniqueFeatureSchema
    )
from disasterpets.Pets.models import (
    Pets, 
    PetsJoin,
    Breeds,
    Gender,
    AlteredStatus,
    PetStatus,
    Animals,
    UniqueFeaturesJoin,
    UniqueFeature,
    )
from disasterpets.Pictures.models import PetImageJoin
from disasterpets.Pictures.schema import PetsImageJoinSchema







def editMatch(requestedData):
    oneEntry = PotentialMatchJoin.query.filter(requestedData['id'] == PotentialMatchJoin.petid).first()
    oneEntry.admincheck = requestedData['admincheck']
    db.session.commit()


def addMatch(requestedData):
    newEntery = PotentialMatchJoin(
        petid = requestedData['id'],
        potentialid = requestedData['potentialid'],
        admincheck = requestedData['match']
    )
    db.session.add(newEntery)
    db.session.commit()


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
                for pet in jresults:
                    pet['features'] = collectAllFeaturesForOnePetbecausetheotheronedontwork(pet)
                    pet['featureID'] = unuiqeFeatureID(pet)
                
                responseObject = {
                    'status' : 'success',
                    'message': 'successfully Pulled!',
                    'pets': jresults,
                    'breeds': breedresult,
                    'genders': genderesults,
                    'animal': animalresults,
                    'status': statusresults,
                    'altered': alteredresults,
                }
                return make_response(jsonify(responseObject)), 201
                
        except Exception as e:
            print(e)
            responseObject = {
                'status' : 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404


def collectAllMatchedID():
    petstat_schema = PotentialMatchJoinSchema(many=True)
    allpetstat = PotentialMatchJoin.query.all()
    statusresults = petstat_schema.dump(allpetstat)
    
    return statusresults



def collectAllMatchForOnePet(requestedData):
    requestedData['id'] = requestedData['petid']
    pet, images, features = collectAllPets(requestedData)
    
    requestedData.pop('id')
    requestedData['id'] = requestedData['potentialid']
    
    pet1, images1, features1 = collectAllPets(requestedData)

    matchedpets = [
        {
            'pet': pet,
            'images': images,
            'feature': features
        },
        {
            'pet': pet1,
            'images': images1,
            'feature': features1
        }
	]

    return matchedpets





class ManageMatchAPI(Resource):
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(PotentialMatchJoin.query.filter_by(id=requestedData['id']).first()):
                editMatch(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'Match Updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No Match found'
                    }
                return make_response(jsonify(responseObject)), 500
            
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
            
            if 'match' in requestedData: # adding role
                
                addMatch(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New Match Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'Match': collectAllMatchForOnePet(requestedData),
                    'message': 'Breed Has Been Returned'
                }
                
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404
    def get(self):
        try:
            MatchedPet = []
            
            allmatchedpets = collectAllMatchedID()
            for pet in allmatchedpets:
                MatchedPet.append(collectAllMatchForOnePet(pet)) 
            
            responseObject = {
                    'status': 'success',
                    'Match': MatchedPet,
                    'message': 'All Matches Have Been Returned'
                }
            return make_response(jsonify(MatchedPet)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404


def unuiqeFeatureID(requestedData):
    data  = UniqueFeaturesJoin.query.filter(requestedData["pet_id"] == UniqueFeaturesJoin.petid).with_entities(UniqueFeaturesJoin.featureid).all()
    Schema = UniqueFeaturesJoinSchema(many = True)
    Results = Schema.dump(data)
    features = []
    
    for featureid in Results:
        toBeFeature = UniqueFeature.query.filter(featureid['featureid'] == UniqueFeature.id).all()
        FeatureNameShema = UniqueFeatureSchema(many = True)
        newfeature = FeatureNameShema.dump(toBeFeature)
        features.append(newfeature)
    return features


def collectAllFeaturesForOnePetbecausetheotheronedontwork(requestedData):
    data  = UniqueFeaturesJoin.query.filter(requestedData["pet_id"] == UniqueFeaturesJoin.petid).with_entities(UniqueFeaturesJoin.featureid).all()
    Schema = UniqueFeaturesJoinSchema(many = True)
    Results = Schema.dump(data)
    features = []

    for featureid in Results:
        toBeFeature = UniqueFeature.query.filter(featureid['featureid'] == UniqueFeature.id).all()
        FeatureNameShema = UniqueFeatureNameSchema(many = True)
        newfeature = FeatureNameShema.dump(toBeFeature)
        features.append(newfeature)
    return features