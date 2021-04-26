from disasterpets.Location.models import Location, LocationJoin
from disasterpets.Pictures.models import PetImage, PetImageJoin
from disasterpets import bcrypt, db, jwt

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
)



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



def collectAllFeaturesForOnePet(requestedData):
    data  = UniqueFeaturesJoin.query.filter(requestedData["id"] == UniqueFeaturesJoin.petid).with_entities(UniqueFeaturesJoin.featureid).all()
    Schema = UniqueFeaturesJoinSchema(many = True)
    Results = Schema.dump(data)
    features = []
    
    for featureid in Results:
        toBeFeature = UniqueFeature.query.filter(featureid['featureid'] == UniqueFeature.id).all()
        FeatureNameShema = UniqueFeatureNameSchema(many = True)
        newfeature = FeatureNameShema.dump(toBeFeature)
        features.append(newfeature)
    return features



def collectAllPets(requestedData):
    pet_schema = PetsSchema(many=True)
    pet_info = (PetImageJoin.query.filter(requestedData["id"] == PetImageJoin.pet_id).with_entities(PetImageJoin.petimage_id).all()) # pet image join ID only
    images = []
    for x in pet_info:
            pet_image = (PetImage.query.filter(PetImage.id == x[0]).with_entities(PetImage.image_url).all()) # pet image url only
            images.append(pet_image) # appends the image url to images
        
    pet_result = Pets.query.filter(requestedData["id"] == Pets.id).all()
    results = pet_schema.dump(pet_result)
    return results, images, collectAllFeaturesForOnePet(requestedData)



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
        petFeature = UniqueFeaturesJoin(petid=pet.id, featureid=feature)
        db.session.add(petFeature)
        db.session.commit()



def addUniqueFeature(requestedData):# TODO this needs to be fixed
    newEntery = UniqueFeature(
        animalid = requestedData['animal'],
        featureid = requestedData['feature'],
        bodyPartid = requestedData['bodyPart'],
        positionid = requestedData['position'],
        colorid = requestedData['color']
        )
    db.session.add(newEntery)
    db.session.commit()
    db.session.refresh(newEntery)
    return newEntery



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

    # for feature in requestedData["features"]:
    #     collectAllFeaturesForOnePet(feature)
    
    db.session.commit()



def collectOnePet(requestedData):
    onePet = Pets.query.filter(requestedData['id'] == Pets.id)
    petsIDSchema = PetsIDSchema(many = True)
    Results = petsIDSchema.dump(onePet)
    
    return Results



def editUniqueFeature(requestedData):# TODO this needs to be fixed
    oneEntry = UniqueFeature.query.filter(requestedData['id'] == UniqueFeature.id).first()
    oneEntry.animalid = requestedData['animal']
    oneEntry.featureid = requestedData['feature']
    oneEntry.bodyPartid = requestedData['bodyPart']
    oneEntry.positionid = requestedData['position']
    oneEntry.colorid = requestedData['color']
    db.session.commit()



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



def editFeature(requestedData):
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



def editBreed(requestedData):
    oneEntry = Breeds.query.filter(requestedData['id'] == Breeds.id).first()
    oneEntry.breed = requestedData['breed']
    db.session.commit()



def addBreed(requestedData):
    newEntery = Breeds(breed = requestedData['breed'])
    db.session.add(newEntery)
    db.session.commit()


def editAlturedStat(requestedData):
    oneEntry = AlteredStatus.query.filter(requestedData['id'] == AlteredStatus.id).first()
    oneEntry.status = requestedData['status']
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
