import os
from flask.json import load
from flask_restful import Resource
from werkzeug.utils import secure_filename
from disasterpets import bcrypt, db, jwt
from disasterpets.Pets.resourceFunctions import(
    addPet,
    addLocation,
    addImage,
    addPetJoin,
    addLocationJoin,
    addPetImageJoin,
    addUniqueFeatureJoin,
    collectAllBreeds,
    collectAllGender,
    collectAllAnimalType,
    collectAllStatus,
    collectAllAlturedStat,
    collectAllFeaturesForOnePet,
    editAlturedStat,
    addAlturedStat,
    collectOneAlturedStat,
    editAnimalType,
    addAnimalType,
    collectOneAnimalType,
    editBreed,
    addBreed,
    collectOneBreed,
    editGender,
    addGender,
    collectOneGender,
    editPetStatus,
    addPetStatus,
    collectOnePetStatus,
    collectAllPetStatus,
    editUniqueFeature,
    addUniqueFeature,
    collectOneUniqueFeature,
    collectAllUniqueFeature,
    editFeature,
    addFeature,
    collectOneFeature,
    collectAllFeature,
    editColor,
    addColor,
    collectOneColor,
    collectAllColor,
    editPosition,
    addPosition,
    collectOnePosition,
    collectAllPosition,
    editBodyPart,
    addBodyPart,
    collectOneBodyPart,
    collectAllBodyPart,
    editPet,
    collectOnePet,
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
    PetImageJoin,
    PetImage
)
class AddPetAPI(Resource):
    def post(self): # adds location and pet and joins
        new_pet = request.get_json()
        current_user = new_pet['user_id']
        try:
            
            pet = addPet(new_pet)
            db.session.refresh(pet)
            
            location = addLocation(new_pet)
            petimage = addImage(new_pet)
            
            addPetJoin(current_user, pet)
            db.session.refresh(pet)
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




class PetDetailAPI(Resource): # TODO NEEDS TO BE REFACTORED
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
                    "feature": collectAllFeaturesForOnePet(this_pet),
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




class ManagePetAPI(Resource): # TODO NEEDS TO BE REFACTORED
    # @jwt_required
    def patch(self):
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
    def post(self):
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




# Patch: EDIT ROLE
# POST: ONE ROLE, NEW
# GET: ALL
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