# from marshmallow import Schema, fields, ValidationError, pre_load, post_load, pre_dump
# from disasterpets import ma
# from disasterpets.Pictures.models import PetImage, PetImageJoin


# class PetImage(ma.Schema):
#     class Meta:
#         model = PetImage
#         fields = ("id", "status")
    
  
# class PetsImageJoin(ma.Schema):
#     class Meta:
#         model = PetImageJoin
#         include_fk = True
#     pet = ma.Function(lambda obj: obj.)
#     primary_breed= ma.Function(lambda obj: obj.pbreed.breed)
#     primary_bid = ma.Function(lambda obj: obj.primary_breed)
#     secondary_breed = ma.Function(lambda obj: obj.sbreed.breed)
#     gender = ma.Function(lambda obj: obj.sex.gender)
#     altered_status = ma.Function(lambda obj: obj.altered.status)
#     animal_type = ma.Function(lambda obj: obj.animal.animal)
#     pet_status = ma.Function(lambda obj: obj.petstatus.status)
#     date_created = ma.Function(lambda obj: obj.date_created)
#     trapper_id = ma.Function(lambda obj: obj.trapper_id)
#     fields = ('id', 'pet_name', 'primary_breed', 'primary_bid', 'secondary_breed',
#         'gender', 'animal_type', 'pet_status', 'altered_status', 'trapper_id', 'date_created')  


