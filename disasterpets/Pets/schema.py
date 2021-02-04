from marshmallow import Schema, fields, ValidationError, pre_load, post_load, pre_dump
from disasterpets import ma
from disasterpets.Pets.models import Breeds, Gender, AlteredStatus, Animals, PetStatus, Pets, PetsJoin



class BreedSchema(ma.Schema):
    class Meta:
        model = Breeds
        fields = ('id', 'breed')
    

class GenderSchema(ma.Schema):
    class Meta:
        model = Gender
        fields = ('id', 'gender')

class AlteredSchema(ma.Schema):
    class Meta:
        fields = ('id', 'status')

class AnimalSchema(ma.Schema):
    class Meta:
        fields = ('id', 'animal')


class PetStatusSchema(ma.Schema):
    class Meta:
        model = PetStatus
        fields = ("id", "status")
    
class PetsJoinSchema(ma.Schema):
    class Meta:
        model = PetsJoin
        fields = ("id", "user_id", "pet_id")


class PetsSchema(ma.Schema):
    class Meta:
        model = Pets
        include_fk = True
    id = ma.Function(lambda obj: obj.id)
    pet_name = ma.Function(lambda obj: obj.pet_name)
    primary_breed= ma.Function(lambda obj: obj.pbreed.breed)
    secondary_breed = ma.Function(lambda obj: obj.sbreed.breed)
    gender = ma.Function(lambda obj: obj.sex.gender)
    altered_status = ma.Function(lambda obj: obj.alteredstat.status)
    animal_type = ma.Function(lambda obj: obj.animal.animal)
    pet_status = ma.Function(lambda obj: obj.pet.pet_status)
    date_created = ma.Function(lambda obj: obj.date_created)
    trapper_id = ma.Function(lambda obj: obj.trapper_id)
    fields = ('id', 'pet_name', 'primary_breed', 'primary_bid', 'secondary_breed',
        'gender', 'animal_type', 'pet_status', 'altered_status', 'trapper_id', 'date_created')  
        
    
