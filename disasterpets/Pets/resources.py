import os
from flask.json import load
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
    UniqueFeaturesJoin,
    Feature,
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
    UniqueFeatureNameSchema,
    BodyPartSchema,
    PositionSchema,
    ColorSchema,
    FeatureSchema,
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


def editPet(requestedData):
    oneEntry = AlteredStatus.query.filter(requestedData['id'] == AlteredStatus.id).first()
    oneEntry.status = requestedData['status']
    db.session.commit()



def addPet(requestedData):
    pet = Pets(
        pet_name=requestedData.get("pet_name"),
        animal_type=requestedData.get("animal_type"),
        primary_breed=requestedData.get("primary_breed"),
        secondary_breed=requestedData.get("secondary_breed"),
        gender=requestedData.get("gender"),
        altered_status=requestedData.get("altered_status"),
        trapper_id=requestedData.get("trapper_id "),
        pet_status=requestedData.get("pet_status"),
        )
    db.session.add(pet)
    db.session.commit()
    return pet



def addLocation(requestedData):
    location = Location(
        street_name=requestedData.get("street_name"),
        house_number=requestedData.get("house_number"),
        city=requestedData.get("city"),
        state=requestedData.get("state"),
        zipcode=requestedData.get("zipcode"),
        )
    db.session.add(location)
    db.session.commit()
    return location


def addImage(requestedData):
    petimage = PetImage(
        image_url=requestedData.get("image_url")
        )
    db.session.add(petimage)
    db.session.commit()
    return petimage


def addPetJoin(current_user, pet):
    petjoin = PetsJoin(user_id=current_user, pet_id=pet.id)
    db.session.add(petjoin)
    db.session.commit()
    return petjoin

def addLocationJoin(location, pet):
    locationjoin = LocationJoin(petid=pet.id, locationid=location.id)
    db.session.add(locationjoin)
    db.session.commit()
    return locationjoin



def addPetImageJoin(pet,petimage):
    petimagejoin = PetImageJoin(pet_id=pet.id, petimage_id=petimage.id)
    db.session.add(petimagejoin)
    db.session.commit()
    return petimagejoin



def collectAllPets():
    pass



def collectOnePet(requestedData):
    oneAlturedStat = AlteredStatus.query.filter(requestedData['id'] == AlteredStatus.id)
    alturedStatSchema = AlteredSchema(many = True)
    Results = alturedStatSchema.dump(oneAlturedStat)
    
    return Results


def collectAllStatus():
    petstat_schema = PetStatusSchema(many=True)
    allpetstat = PetStatus.query.all()
    statusresults = petstat_schema.dump(allpetstat)
    
    return statusresults
















def addUniqueFeatureJoin(pet, new_pet):
    for feature in new_pet['feature']:
        feature = addUniqueFeature(feature).id
        db.session.refresh(feature)
        petFeature = UniqueFeaturesJoinSchema(petid=pet.id, featureid=feature.id)
        db.session.add(petFeature)
        db.session.commit()























class AddPetAPI(Resource): # TODO make so it takes more than one image
    def post(self): # adds location and pet and joins
        new_pet = request.get_json()
        current_user = get_jwt_identity()
        try:
            
            pet = addPet(new_pet)
            db.session.refresh(pet)
            
            location = addLocation(new_pet)
            petimage = addImage(new_pet)
            
            addPetJoin(current_user, pet)
            # db.session.refresh(pet)
            db.session.refresh(location)
            
            addLocationJoin(pet, location)
            db.session.refresh(pet)
            db.session.refresh(petimage)
            
            addPetImageJoin(pet,petimage)
            
            addUniqueFeatureJoin(pet, new_pet)
            
            
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

    def get(self): # gets everything a pet can have (general call is not tied to a pet)
        try:
            responseObject = {
                "status": "success",
                "message": "successfully Pulled!",
                "breeds": collectAllBreeds(),
                "genders": collectAllGender(),
                "animal": collectAllAnimalType(),
                "status": collectAllStatus(),
                "altered": collectAllAlturedStat(),
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
    def post(self): # one pet
        this_pet = request.get_json()
        pet_schema = PetsSchema(many=True)
        
        try:
            pet_info = (PetImageJoin.query.filter(this_pet["id"] == PetImageJoin.pet_id).with_entities(PetImageJoin.petimage_id).all()) # pet image join ID only
            images = []
            for x in pet_info:
                pet_image = (PetImage.query.filter(PetImage.id == x[0]).with_entities(PetImage.image_url).all()) # pet image url only
                images.append(pet_image) # appends the image url to images
            
            pet_result = Pets.query.filter(this_pet["id"] == Pets.id).all()
            results = pet_schema.dump(pet_result)
            
            if pet_info == None:
                responseObject = {
                    "status": "error",
                    "message": "no pet found"
                }
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
n(pet, new_pet):
    petimagejoin = UniqueFeaturesJoinSchema(petid=pet.id, featureid=addUniqueFeature(new_pet).id)
    db.session.add(petimagejoin)
    db.session.commit()ef editAlturedStat(requestedData):
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



class ManageUniqueFeaturesAPI(Resource):
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(UniqueFeature.query.filter_by(id=requestedData['id']).first()):
                editUniqueFeature(requestedData)
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
                
                addUniqueFeature(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New Feature Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'Feature': collectOneUniqueFeature(requestedData),
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
                    'Feature': collectAllUniqueFeature(),
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



def editUniqueFeature(requestedData):# TODO this needs to be fixed
    oneEntry = UniqueFeature.query.filter(requestedData['id'] == UniqueFeature.id).first()
    oneEntry.animalid = requestedData['animal']
    oneEntry.featureid = requestedData['feature']
    oneEntry.bodyPartid = requestedData['bodyPart']
    oneEntry.positionid = requestedData['position']
    oneEntry.colorid = requestedData['color']
    db.session.commit()



def addUniqueFeature(requestedData):# TODO this needs to be fixed
    newEntery = UniqueFeature(
        animal = requestedData['animal'],
        feature = requestedData['feature'],
        bodyPart = requestedData['bodyPart'],
        position = requestedData['position'],
        color = requestedData['color']
        )
    db.session.add(newEntery)
    db.session.commit()
    return newEntery



def collectOneUniqueFeature(requestedData):# TODO this needs to be fixed
    oneFeature = UniqueFeature.query.filter(requestedData['id'] == UniqueFeature.id)
    Schema = UniqueFeatureSchema(many = True)
    Results = Schema.dump(oneFeature)
    
    return Results



def collectAllUniqueFeature():# TODO this needs to be fixed
    Schema = UniqueFeatureNameSchema(many = True)
    
    allFeature = UniqueFeature.query.all()
    Results = Schema.dump(allFeature)
    return Results



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL



class ManageFeaturesAPI(Resource):
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(Feature.query.filter_by(id=requestedData['id']).first()):
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



def editFeature(requestedData):
    pass
    oneEntry = Feature.query.filter(requestedData['id'] == Feature.id).first()
    oneEntry.feature = requestedData['feature']
    db.session.commit()



def addFeature(requestedData):# TODO this needs to be fixed
    
    newEntery = Feature(
        feature = requestedData['feature']
        )
    db.session.add(newEntery)
    db.session.commit()



def collectOneFeature(requestedData):# TODO this needs to be fixed
    oneFeature = Feature.query.filter(requestedData['id'] == Feature.id)
    Schema = FeatureSchema(many = True)
    Results = Schema.dump(oneFeature)
    
    return Results



def collectAllFeature():# TODO this needs to be fixed
    
    Schema = FeatureSchema(many = True)
    allFeatures = Feature.query.all()
    Results = Schema.dump(allFeatures)
    return Results



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL



class ManageColorsAPI(Resource):
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(Colors.query.filter_by(id=requestedData['id']).first()):
                editColor(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'Color Updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No Color found'
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
            
            if 'color' in requestedData: # adding role
                
                addColor(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New Color Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'Color': collectOneColor(requestedData),
                    'message': 'Color Has Been Returned'
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
                    'Color': collectAllColor(),
                    'message': 'All Colors Have Been Returned'
                }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404



def editColor(requestedData):# TODO this needs to be fixed
    oneEntry = Colors.query.filter(requestedData['id'] == Colors.id).first()
    oneEntry.color = requestedData['color']
    db.session.commit()



def addColor(requestedData):# TODO this needs to be fixed
    
    newEntery = Colors(
        color = requestedData['color']
        )
    db.session.add(newEntery)
    db.session.commit()



def collectOneColor(requestedData):# TODO this needs to be fixed
    oneColor = Colors.query.filter(requestedData['id'] == Colors.id)
    Schema = ColorSchema(many = True)
    Results = Schema.dump(oneColor)
    
    return Results



def collectAllColor():# TODO this needs to be fixed
    
    Schema = ColorSchema(many = True)
    allColor = Colors.query.all()
    Results = Schema.dump(allColor)
    return Results



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL








class ManagePositionsAPI(Resource):
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(Positions.query.filter_by(id=requestedData['id']).first()):
                editPosition(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'Position Updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No Position found'
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
            
            if 'position' in requestedData: # adding role
                
                addPosition(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New Position Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'Position': collectOnePosition(requestedData),
                    'message': 'Position Has Been Returned'
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
                    'Position': collectAllPosition(),
                    'message': 'All Positions Have Been Returned'
                }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404



def editPosition(requestedData):# TODO this needs to be fixed
    oneEntry = Positions.query.filter(requestedData['id'] == Positions.id).first()
    oneEntry.position = requestedData['position']
    db.session.commit()



def addPosition(requestedData):# TODO this needs to be fixed
    
    newEntery = Positions(
        position = requestedData['position']
        )
    db.session.add(newEntery)
    db.session.commit()



def collectOnePosition(requestedData):# TODO this needs to be fixed
    onePosition = Positions.query.filter(requestedData['id'] == Positions.id)
    Schema = PositionSchema(many = True)
    Results = Schema.dump(onePosition)
    
    return Results



def collectAllPosition():# TODO this needs to be fixed
    
    Schema = PositionSchema(many = True)
    allPosition = Positions.query.all()
    Results = Schema.dump(allPosition)
    return Results



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL




class ManageBodyPartsAPI(Resource):
    # @jwt_required
    def patch(self):
        try:
            requestedData = request.get_json()
            if bool(BodyParts.query.filter_by(id=requestedData['id']).first()):
                editBodyPart(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'BodyPart Updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No BodyPart found'
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
            
            if 'bodyPart' in requestedData: # adding role
                addBodyPart(requestedData)
                responseObject = {
                    'status': 'success',
                    'message': 'New BodyPart Has been Added'
                }
                
            else: # giving back one the roles
                
                responseObject = {
                    'status': 'success',
                    'BodyPart': collectOneBodyPart(requestedData),
                    'message': 'BodyPart Has Been Returned'
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
                    'BodyPart': collectAllBodyPart(),
                    'message': 'All BodyParts Have Been Returned'
                }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404



def editBodyPart(requestedData):
    oneEntry = BodyParts.query.filter(requestedData['id'] == BodyParts.id).first()
    oneEntry.bodypart = requestedData['bodyPart']
    db.session.commit()



def addBodyPart(requestedData):# TODO this needs to be fixed
    
    newEntery = BodyParts(
        bodypart = requestedData['bodyPart']
        )
    db.session.add(newEntery)
    db.session.commit()



def collectOneBodyPart(requestedData):# TODO this needs to be fixed
    oneBodyPart = BodyParts.query.filter(requestedData['id'] == BodyParts.id)
    Schema = BodyPartSchema(many = True)
    Results = Schema.dump(oneBodyPart)
    
    return Results



def collectAllBodyPart():# TODO this needs to be fixed
    
    Schema = BodyPartSchema(many = True)
    allBodyPart = BodyParts.query.all()
    Results = Schema.dump(allBodyPart)
    return Results



# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL





class UniqueFeaturesInfoAPI(Resource):
    # @jwt_required
    def get(self):
        try:
            responseObject = {
                    'status': 'success',
                    'animal':collectAllAnimalType(),
                    'color': collectAllColor(),
                    'feature':collectAllFeature(),
                    'position':collectAllPosition(),
                    'BodyPart': collectAllBodyPart(),
                    'message': 'All BodyParts Have Been Returned'
                }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404