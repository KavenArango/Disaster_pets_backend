
import os
from flask_restful import Resource
from disasterpets import bcrypt, db, jwt
from werkzeug.utils import secure_filename
from disasterpets.Location.models import Location, LocationJoin
from disasterpets.Pictures.models import PetImage, PetImageJoin
from disasterpets.Pets.models import Pets, PetsJoin, Breeds, Gender, AlteredStatus, PetStatus, Animals
from flask import Flask, Blueprint, jsonify, request, make_response, current_app, session, url_for, app
from disasterpets.Pets.schema import PetsSchema, BreedSchema, GenderSchema, PetStatusSchema, AnimalSchema, AlteredSchema
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
# from disasterpets.Pets.models import Pets, PetsJoin


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
                trapper_id =new_pet.get('trapper_id '),
                pet_status = new_pet.get('pet_status')

            )
            db.session.add(pet)
            db.session.commit()

            location = Location(
                street_name=new_pet.get('street_name'),
                house_number = new_pet.get('house_number'),
                city = new_pet.get('city'),
                state = new_pet.get('state'),
                zipcode = new_pet.get('zipcode')
            )
            db.session.add(location)
            db.session.commit()

            petimage = PetImage(
                image_url = new_pet.get('image_url')
            )
            db.session.add(petimage)
            db.session.commit()

            db.session.refresh(pet)
            petjoin = PetsJoin(
                user_id = current_user,
                pet_id = pet.id
            )
            db.session.add(petjoin)
            db.session.commit()

            db.session.refresh(pet)
            db.session.refresh(location)
            locationjoin = LocationJoin(
                petid = pet.id,
                locationid=location.id
            )
            db.session.add(locationjoin)
            db.session.commit()

            db.session.refresh(pet)
            db.session.refresh(petimage)
            petimagejoin = PetImageJoin(
                pet_id = pet.id,
                petimage_id = petimage.id
            )
            db.session.add(petimagejoin)
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

    @jwt_required
    def get(self):
        breeds_schema = BreedSchema(many=True)
        genders_schema = GenderSchema(many = True)
        petstat_schema = PetStatusSchema(many =True)
        animals_schena = AnimalSchema(many=True)
        altered_schema = AlteredSchema(many=True)
        try:
            allbreeds = Breeds.query.all()
            breedresult = breeds_schema.dump(allbreeds)
            allgenders = Gender.query.all()
            genderesults = genders_schema.dump(allgenders)
            allpetstat = PetStatus.query.all()
            statusresults = petstat_schema.dump(allpetstat)
            allanimals = Animals.query.all()
            animalresults = animals_schena.dump(allanimals)
            altered = AlteredStatus.query.all()
            alteredresults = altered_schema.dump(altered)
            responseObject = {
                'status' : 'success',
                'message': 'successfully Pulled!',
                'breeds': breedresult,
                'genders': genderesults,
                'animal': animalresults,
                'status': statusresults,
                'altered': alteredresults
            }
            return make_response(jsonify(responseObject)), 201
                    
    
        except Exception as e:
                print(e)
                responseObject = {
                    'status' : 'failed',
                    'message': 'something went wrong try again'
                }
                return make_response(jsonify(responseObject)), 404


class PetDetailAPI(Resource):
    @jwt_required
    def get(self, pet_id):
        this_pet = request.get_json()

        pet_schema = PetsSchema(many = True)

        try:
            pet_info = PetImageJoin.query.filter(this_pet['id'] == PetImageJoin.pet_id).with_entities(PetImageJoin.petimage_id).all()

            images = []
            for x in pet_info:
                pet_image = PetImage.query.filter(PetImage.id == x[0]).with_entities(PetImage.image_url).all()
                images.append(pet_image)

            pet_result = Pets.query.all()
            jresults = pet_schema.dump(pet_result)
            
            if pet_info == None:
                responseObject = {
                'status': 'error',
                'message': 'no pet found'
                }
                return make_response(jsonify(responseObject)), 500
            else:
                responseObject = {
                'status': 'success',
                'images': images,
                'pet': jresults,
                'message': 'successfully added pet'
                }
                return make_response(jsonify(responseObject)), 201

        except Exception as e:
                print(e)
                responseObject = {
                    'status' : 'failed',
                    'message': 'something went wrong try again'
                }
                return make_response(jsonify(responseObject)), 404


class UploadImageAPI(Resource):
    @jwt_required
    def post(self):
        target=os.path.join('static/images')
        if not os.path.isdir(target):
            responseObject = {
                'status': 'error',
                'message': 'something went wrong'
            }
            return make_response(jsonify(responseObject)), 500
        print(request)
        fileObj = request.files
        for f in fileObj:
            file = request.files.get(f)
            filename = secure_filename(file.filename)
            file.save(os.path.join(target, filename))
        responseObject = {
                'status': 'success',
                'message': 'successfully added photo',
                'url': "http://localhost:5000/" + filename
        }
        return make_response(jsonify(responseObject)), 200








def editPet(requestedData):
    onePet = Pets.query.filter(requestedData['id'] == '1').first()
    
    # onePet.fname = requestedData['fname']

    db.session.commit()



















class ManagePetAPI(Resource):
    # @jwt_required
    def get(self):  # taking from client giving to db
        try:
            requestedData = request.get_json()
            editPet(requestedData)
            
            onePet = Pets.query.filter(requestedData['id'] == '1').first()
            
            
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