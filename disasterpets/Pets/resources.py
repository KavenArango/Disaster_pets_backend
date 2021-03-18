import os
from flask_restful import Resource
from disasterpets import bcrypt, db, jwt
from werkzeug.utils import secure_filename
from disasterpets.Location.models import Location, LocationJoin
from disasterpets.Pictures.models import PetImage, PetImageJoin
from disasterpets.Pets.models import (
    Pets,
    PetsJoin,
    Breeds,
    Gender,
    AlteredStatus,
    PetStatus,
    Animals,
    UniqueFeature,
    BodyParts,
    Positions,
    Colors,
    UniqueFeaturesJoin
)
from disasterpets.Pets.schema import (
    PetsSchema,
    BreedSchema,
    GenderSchema,
    PetStatusSchema,
    AnimalSchema,
    AlteredSchema,
    PetsIDSchema,
    UniqueFeatureSchema,
    UniqueFeaturesJoinSchema,
    BodyPartSchema,
    PositionSchema,
    ColorSchema,
)
from flask import (
    Flask,
    Blueprint,
    jsonify,
    request,
    make_response,
    current_app,
    session,
    url_for,
    app,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)

# from disasterpets.Pets.models import Pets, PetsJoin


class AddPetAPI(Resource):
    def post(self):
        new_pet = request.get_json()
        current_user = get_jwt_identity()
        try:
            pet = Pets(
                pet_name=new_pet.get("pet_name"),
                animal_type=new_pet.get("animal_type"),
                primary_breed=new_pet.get("primary_breed"),
                secondary_breed=new_pet.get("secondary_breed"),
                gender=new_pet.get("gender"),
                altered_status=new_pet.get("altered_status"),
                trapper_id=new_pet.get("trapper_id "),
                pet_status=new_pet.get("pet_status"),
            )
            db.session.add(pet)
            db.session.commit()

            location = Location(
                street_name=new_pet.get("street_name"),
                house_number=new_pet.get("house_number"),
                city=new_pet.get("city"),
                state=new_pet.get("state"),
                zipcode=new_pet.get("zipcode"),
            )
            db.session.add(location)
            db.session.commit()

            petimage = PetImage(image_url=new_pet.get("image_url"))
            db.session.add(petimage)
            db.session.commit()

            db.session.refresh(pet)
            petjoin = PetsJoin(user_id=current_user, pet_id=pet.id)
            db.session.add(petjoin)
            db.session.commit()

            db.session.refresh(pet)
            db.session.refresh(location)
            locationjoin = LocationJoin(petid=pet.id, locationid=location.id)
            db.session.add(locationjoin)
            db.session.commit()

            db.session.refresh(pet)
            db.session.refresh(petimage)
            petimagejoin = PetImageJoin(pet_id=pet.id, petimage_id=petimage.id)
            db.session.add(petimagejoin)
            db.session.commit()

            responseObject = {
                "status": "success",
                "message": "successfully added pet"
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            print(e)
            responseObject = {
                "status": "failed",
                "message": "something went wrong try again",
            }
            return make_response(jsonify(responseObject)), 404

    def get(self):
        breeds_schema = BreedSchema(many=True)
        genders_schema = GenderSchema(many=True)
        petstat_schema = PetStatusSchema(many=True)
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
                "status": "success",
                "message": "successfully Pulled!",
                "breeds": breedresult,
                "genders": genderesults,
                "animal": animalresults,
                "status": statusresults,
                "altered": alteredresults,
            }
            return make_response(jsonify(responseObject)), 201

        except Exception as e:
            print(e)
            responseObject = {
                "status": "failed",
                "message": "something went wrong try again",
            }
            return make_response(jsonify(responseObject)), 404


class PetDetailAPI(Resource):
    def post(self):
        this_pet = request.get_json()

        pet_schema = PetsSchema(many=True)

        try:
            pet_info = (PetImageJoin.query.filter(
                this_pet["id"] == PetImageJoin.pet_id).with_entities(
                    PetImageJoin.petimage_id).all())

            images = []
            for x in pet_info:
                pet_image = (PetImage.query.filter(
                    PetImage.id == x[0]).with_entities(
                        PetImage.image_url).all())
                images.append(pet_image)

            pet_result = Pets.query.filter(this_pet["id"] == Pets.id).all()
            results = pet_schema.dump(pet_result)

            if pet_info == None:
                responseObject = {"status": "error", "message": "no pet found"}
                return make_response(jsonify(responseObject)), 500
            else:
                responseObject = {
                    "status": "success",
                    "images": images,
                    "pets": results,
                    "message": "single pet has been returned",
                }
                return make_response(jsonify(responseObject)), 201

        except Exception as e:
            print(e)
            responseObject = {
                "status": "failed",
                "message": "something went wrong try again",
            }
            return make_response(jsonify(responseObject)), 404


class UploadImageAPI(Resource):
    def post(self):
        target = os.path.join("static/images")
        if not os.path.isdir(target):
            responseObject = {
                "status": "error",
                "message": "something went wrong"
            }
            return make_response(jsonify(responseObject)), 500
        print(request)
        fileObj = request.files
        for f in fileObj:
            file = request.files.get(f)
            filename = secure_filename(file.filename)
            file.save(os.path.join(target, filename))
        responseObject = {
            "status": "success",
            "message": "successfully added photo",
            "url": "http://localhost:5000/" + filename,
        }
        return make_response(jsonify(responseObject)), 200



def editPet(requestedData):
    onePet = Pets.query.filter(requestedData['id'] == Pets.id).first()
    
    onePet.pet_name = requestedData["pet_name"]
    onePet.pet_status = requestedData["pet_status"]
    onePet.altered_status = requestedData["altered_status"]
    onePet.animal_type = requestedData["animal_type"]
    onePet.gender = requestedData["gender"]
    onePet.primary_breed = requestedData["primary_breed"]
    onePet.secondary_breed = requestedData["secondary_breed"]
    onePet.trapper_id = requestedData["trapper_id"]

    db.session.commit()



def collectOnePet(requestedData):
    onePet = Pets.query.filter(requestedData['id'] == Pets.id)
    petsIDSchema = PetsIDSchema(many = True)
    Results = petsIDSchema.dump(onePet)
    
    return Results



class ManagePetAPI(Resource):
    # @jwt_required
    def patch(self):  # taking from client giving to db
        try:
            requestedData = request.get_json()
            
            if bool(PetsJoin.query.filter_by(id=requestedData['id']).first()):
                editPet(requestedData)
                responseObject = {
                    "status": "success", 
                    "message": "Pet updated"
                    }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    "status": "error", 
                    "message": "Pet not found"
                    }
                return make_response(jsonify(responseObject)), 500
        except Exception as e:
            print(e)
            responseObject = {
                "status": "failed",
                "message": "something went wrong try again",
            }
            return make_response(jsonify(responseObject)), 404
    def post(sefl):
        try:
            requestedData = request.get_json()
            if bool(Pets.query.filter_by(id=requestedData['id']).first()):
                
                responseObject = {
                    "status": "success",
                    "Pet": collectOnePet(requestedData),
                    "message": "Pet Returned"
                    }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    "status": "error", 
                    "message": "Pet not found"
                    }
                return make_response(jsonify(responseObject)), 500
        except Exception as e:
            print(e)
            responseObject = {
                "status": "failed",
                "message": "something went wrong try again",
            }
            return make_response(jsonify(responseObject)), 404




def editAlturedStat(requestedData):
    oneEntry = AlteredStatus.query.filter(requestedData['id'] == AlteredStatus.id).first()
    oneEntry.status = requestedData['status']
    db.session.commit()



def addAlturedStat(requestedData):
    newEntery = AlteredStatus(status = requestedData['status'])
    db.session.add(newEntery)
    db.session.commit()



def collectOneAlturedStat(requestedData):
    oneAlturedStat = AlteredStatus.query.filter(requestedData['id'] == AlteredStatus.id)
    alturedStatSchema = AlteredSchema(many = True)
    Results = alturedStatSchema.dump(oneAlturedStat)
    
    return Results



def collectAllAlturedStat():
    
    alturedStatSchema = AlteredSchema(many = True)
    allAlturedStat = AlteredStatus.query.all()
    alturedStatResults = alturedStatSchema.dump(allAlturedStat)
    return alturedStatResults



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL


class ManageAlteredStatAPI(Resource):
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(AlteredStatus.query.filter_by(id=requestedData['id']).first()):
                print("HELLO")
                editAlturedStat(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'Altured Status Updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No Altered Status found'
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
            
            if 'status' in requestedData: # adding role
                
                addAlturedStat(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New Altered Status Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'AlteredStatus': collectOneAlturedStat(requestedData),
                    'message': 'Single Altered Status Have Been Returned'
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
            responseObject = {
                    'status': 'success',
                    'AlteredStatus': collectAllAlturedStat(),
                    'message': 'All Altered Statuses Have Been Returned'
                }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404



def editAnimalType(requestedData):
    oneEntry = Animals.query.filter(requestedData['id'] == Animals.id).first()
    oneEntry.animal = requestedData['animal']
    db.session.commit()



def addAnimalType(requestedData):
    newEntery = Animals(animal = requestedData['animal'])
    db.session.add(newEntery)
    db.session.commit()



def collectOneAnimalType(requestedData):
    oneAnimalType = Animals.query.filter(requestedData['id'] == Animals.id)
    animalSchema = AnimalSchema(many = True)
    Results = animalSchema.dump(oneAnimalType)
    
    return Results



def collectAllAnimalType():
    
    animalSchema = AnimalSchema(many = True)
    allAnimalType = Animals.query.all()
    Results = animalSchema.dump(allAnimalType)
    return Results



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL


class ManageAnimalTypeAPI(Resource):
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(Animals.query.filter_by(id=requestedData['id']).first()):
                editAnimalType(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'Animal Type Updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No Animal Type found'
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
            
            if 'animal' in requestedData: # adding role
                
                addAnimalType(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New Animal Type Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'AnimalTypes': collectOneAnimalType(requestedData),
                    'message': 'Single Animal Types Have Been Returned'
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
            responseObject = {
                    'status': 'success',
                    'AnimalType': collectAllAnimalType(),
                    'message': 'All Animal Types Have Been Returned'
                }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404












def editBreed(requestedData):
    oneEntry = Breeds.query.filter(requestedData['id'] == Breeds.id).first()
    oneEntry.breed = requestedData['breed']
    db.session.commit()



def addBreed(requestedData):
    newEntery = Breeds(breed = requestedData['breed'])
    db.session.add(newEntery)
    db.session.commit()



def collectOneBreed(requestedData):
    oneBreed = Breeds.query.filter(requestedData['id'] == Breeds.id)
    breedSchema = BreedSchema(many = True)
    Results = breedSchema.dump(oneBreed)
    
    return Results



def collectAllBreeds():
    
    breedSchema = BreedSchema(many = True)
    allBreeds = Breeds.query.all()
    Results = breedSchema.dump(allBreeds)
    return Results



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL


class ManageBreedsAPI(Resource):
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(Breeds.query.filter_by(id=requestedData['id']).first()):
                editBreed(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'Breed Updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No Breed found'
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
            
            if 'breed' in requestedData: # adding role
                
                addBreed(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New Breed Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'Breed': collectOneBreed(requestedData),
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
            responseObject = {
                    'status': 'success',
                    'Breeds': collectAllBreeds(),
                    'message': 'All Breeds Have Been Returned'
                }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404


def editGender(requestedData):
    oneEntry = Gender.query.filter(requestedData['id'] == Gender.id).first()
    oneEntry.gender = requestedData['gender']
    db.session.commit()



def addGender(requestedData):
    newEntery = Gender(gender = requestedData['gender'])
    db.session.add(newEntery)
    db.session.commit()



def collectOneGender(requestedData):
    oneGender = Gender.query.filter(requestedData['id'] == Gender.id)
    genderSchema = GenderSchema(many = True)
    Results = genderSchema.dump(oneGender)
    
    return Results



def collectAllGender():
    
    genderSchema = GenderSchema(many = True)
    allGender = Gender.query.all()
    Results = genderSchema.dump(allGender)
    return Results



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL


class ManageGenderAPI(Resource):
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(Gender.query.filter_by(id=requestedData['id']).first()):
                editGender(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'Gender Updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No Gender found'
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
            
            if 'gender' in requestedData: # adding role
                
                addGender(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New Gender Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'Genders': collectOneGender(requestedData),
                    'message': 'Gender Has Been Returned'
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
            responseObject = {
                    'status': 'success',
                    'Genders': collectAllGender(),
                    'message': 'All Genders Have Been Returned'
                }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404




def editPetStatus(requestedData):
    oneEntry = PetStatus.query.filter(requestedData['id'] == PetStatus.id).first()
    oneEntry.status = requestedData['status']
    db.session.commit()



def addPetStatus(requestedData):
    newEntery = PetStatus(status = requestedData['status'])
    db.session.add(newEntery)
    db.session.commit()



def collectOnePetStatus(requestedData):
    onePetStatus = PetStatus.query.filter(requestedData['id'] == PetStatus.id)
    petStatusSchema = PetStatusSchema(many = True)
    Results = petStatusSchema.dump(onePetStatus)
    
    return Results



def collectAllPetStatus():
    
    petStatusSchema = PetStatusSchema(many = True)
    allPetStatus = PetStatus.query.all()
    Results = petStatusSchema.dump(allPetStatus)
    return Results



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL

class ManagePetStatusAPI(Resource):
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(PetStatus.query.filter_by(id=requestedData['id']).first()):
                editPetStatus(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'Pet Status Updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No Pet Status found'
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
            
            if 'status' in requestedData: # adding role
                
                addPetStatus(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New Pet Status Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'Status': collectOnePetStatus(requestedData),
                    'message': 'Pet Status Has Been Returned'
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
            responseObject = {
                    'status': 'success',
                    'Status': collectAllPetStatus(),
                    'message': 'All Pet Status Have Been Returned'
                }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404


















































class ManageFeaturesAPI():
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(Breeds.query.filter_by(id=requestedData['id']).first()): # TODO this needs to be fixed
                editFeature(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'Feature Updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No Feature found'
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
            
            if 'feature' in requestedData: # adding role
                
                addFeature(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New Feature Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'Feature': collectOneFeature(requestedData),
                    'message': 'Feature Has Been Returned'
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
            responseObject = {
                    'status': 'success',
                    'Feature': collectAllFeature(),
                    'message': 'All Features Have Been Returned'
                }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404









def editFeature(requestedData):# TODO this needs to be fixed
    oneEntry = PetStatus.query.filter(requestedData['id'] == PetStatus.id).first()
    oneEntry.status = requestedData['status']
    db.session.commit()



def addFeature(requestedData):# TODO this needs to be fixed
    
    newEntery = PetStatus(status = requestedData['status'])
    db.session.add(newEntery)
    db.session.commit()



def collectOneFeature(requestedData):# TODO this needs to be fixed
    onePetStatus = PetStatus.query.filter(requestedData['id'] == PetStatus.id)
    petStatusSchema = PetStatusSchema(many = True)
    Results = petStatusSchema.dump(onePetStatus)
    
    return Results



def collectAllFeature():# TODO this needs to be fixed
    
    petStatusSchema = PetStatusSchema(many = True)
    allPetStatus = PetStatus.query.all()
    Results = petStatusSchema.dump(allPetStatus)
    return Results



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL
