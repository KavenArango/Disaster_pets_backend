from marshmallow import Schema, fields, ValidationError, pre_load, post_load, pre_dump
from disasterpets import ma
from disasterpets.Pictures.models import PetImage, PetImageJoin


class PetImageSchema(ma.Schema):
    class Meta:
        model = PetImage
        fields = ("id", "status")
    
  
class PetsImageJoinSchema(ma.Schema):
    class Meta:
        model = PetImageJoin
        include_fk = True
    pet_name = ma.Function(lambda obj: obj.pet.pet_name)
    primary_breed= ma.Function(lambda obj: obj.pet.primary_breed)
    secondary_breed = ma.Function(lambda obj: obj.secondary_breed)
    gender = ma.Function(lambda obj: obj.pet.gender)
    altered_status = ma.Function(lambda obj: obj.pet.altered_status)
    animal_type = ma.Function(lambda obj: obj.pet.animal)
    pet_status = ma.Function(lambda obj: obj.pet.status)
    date_created = ma.Function(lambda obj: obj.pet.date_created)
    trapper_id = ma.Function(lambda obj: obj.pet.trapper_id)
    pet_image = ma.Function(lambda obj: obj.petimage.image_url)
    fields = ('id', 'pet_name', 'primary_breed', 'primary_bid', 'secondary_breed',
        'gender', 'animal_type', 'pet_status', 'altered_status', 'trapper_id', 'date_created', 'pet_image')  


