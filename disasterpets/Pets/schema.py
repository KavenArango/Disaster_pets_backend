from marshmallow import Schema, fields, ValidationError, pre_load, post_load, pre_dump
from disasterpets import ma
from disasterpets.Pets.models import Breeds, Gender, AlteredStatus, Animals, PetStatus, Pets



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
        
    
   




# class BreedSchema(Schema):
#     id = fields.Int(dump_only = True)
#     breed = fields.Str()
#     format_breed = fields.Method("format_breed", dump_only = True)

#     def format_breed(self, breed):
#         return "{}".format(breed.breed)

    

# class GenderSchema(Schema):
#     id = fields.Int(dump_only = True)
#     gender = fields.Str()
#     format_gender = fields.Method("format_gender", dump_only = True)

#     def format_gender(self, gender):
#         return "{}".format(genders.gender)

#     def inherit_from_parent(gender, context):
#         gender['id'] = context['gender']
#         return gender

# class AlteredSchema(Schema):
#     id = fields.Int(dump_only=True)
#     status = fields.Str()
#     format_altered = fields.Method("format_altered", dump_only = True)

#     def format_altered(self, status):
#         return "{}".format(status.status)

# class AnimalSchema(Schema):
#     id = fields.Int(dump_only=True)
#     animal = fields.Str()
#     format_animal = fields.Method("format_animal", dump_only = True)

#     def format_animal(self, animal):
#         return "{}".format(Animals.animal)
    

# class PetStatusSchema(Schema):
#     id = fields.Int(dump_only=True)
#     status = fields.Str()
#     format_petstatus = fields.Method("format_petstatus", dump_only = True)

#     def format_petstatus(self, status):
#         return "{}".format(PetStatus.status)
    


# class Pet:
#     def __init__(self, name, an, pbreed, sbreed, gen, astat, ps, tid, date):
#         self.name = name 
#         self.an = an
#         self.pbreed = pbreed
#         self.sbreed = sbreed
#         self.gen = gen
#         self.astat = astat
#         self.ps = ps
#         self.tid = tid
#         self.date = sale.date

#     def __repr__(self):
#         return "{}, {}, {}, {}, {}, {}, {}, {}".format(name, an, pbreed, sbreed, gen, astat, ps, tid, date)

# class PetsSchema(Schema):
#     id = fields.Int(dump_only=True)
#     pet_name = fields.Str()
#     animal_type = fields.Nested(AnimalSchema, only=("animal",), validate=must_not_be_blank)
#     primary_breed = fields.Nested(BreedSchema, only=("breed",), validate=must_not_be_blank)
#     secondary_breed = fields.Nested(BreedSchema, only=("breed",), validate=must_not_be_blank)
#     gender = fields.Nested(GenderSchema, only=("gender",), validate=must_not_be_blank)
#     altered_status = fields.Nested(AlteredSchema,only=("status",), validate=must_not_be_blank)
#     pet_status = fields.Nested(PetStatusSchema,only=("status",), validate=must_not_be_blank)
#     trapper_id = fields.Str()
#     date_created = fields.Str()
   

#     @pre_dump
#     def set_context(self, pet, **kwargs):
#         self.context['gender'] = pet['id']
#         return data

