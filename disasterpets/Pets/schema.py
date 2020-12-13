from marshmallow import Schema, fields, ValidationError, pre_load
from disasterpets import ma
from disasterpets.Pets.models import Breeds, Gender, AlteredStatus, Animals, PetStatus, Pets


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


# class BreedSchema(ma.Schema):
#     class Meta:
#         model = Breeds
#         fields = ('id', 'breed')
#     # format_breed = fields.Method("format_breed", dump_only = True)

#     # def format_breed(self, breed):
#     #     return (breed.breed)

# class GenderSchema(ma.Schema):
#     class Meta:
#         model = Gender
#         fields = ('id', 'gender')

# class AlteredSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'status')

# class AnimalSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'animal')


# class PetStatusSchema(ma.Schema):
#     class Meta:
#         model = PetStatus
#         fields = ("id", "status")
    
  
# class PetsSchema(ma.Schema):
#     class Meta:
#         model = Pets
#         fields = ('id', 'pet_name', 'trapper_id', 'date_created')  
#     primary_breed = ma.Nested(BreedSchema)
#     secondary_breed = ma.Nested(BreedSchema) 
#     gender = ma.Nested(GenderSchema) 
#     altered_status = ma.Nested(AlteredSchema) 
#     animal_type = ma.Nested(AnimalSchema)  
#     pet_status = ma.Nested(PetStatusSchema) 
#     format_pet= fields.Method("format_pet", dump_only=True)

#     def format_pet(self, pets):
#         return (Pets.pet_name, Pets.animal_type, Pets.primary_breed, 
#         Pets.secondary_breed, Pets.gender, Pets.pet_status, Pets.altered_status, Pets.trapper_id, Pets.date_created)

   


class BreedSchema(Schema):
    id = fields.Int(dump_only = True)
    breed = fields.Str()
    format_breed = fields.Method("format_breed", dump_only = True)

    def format_breed(self, breed):
        return "{}".format(breed.breed)

class GenderSchema(Schema):
    id = fields.Int(dump_only = True)
    gender = fields.Str()
    format_gender = fields.Method("format_gender", dump_only = True)

    def format_gender(self, gender):
        return "{}".format(genders.gender)

class AlteredSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Str()
    format_altered = fields.Method("format_altered", dump_only = True)

    def format_altered(self, status):
        return "{}".format(status.status)

class AnimalSchema(Schema):
    id = fields.Int(dump_only=True)
    animal = fields.Str()
    format_animal = fields.Method("format_animal", dump_only = True)

    def format_animal(self, animal):
        return "{}".format(Animals.animal)
    

class PetStatusSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Str()
    format_petstatus = fields.Method("format_petstatus", dump_only = True)

    def format_petstatus(self, status):
        return "{}".format(PetStatus.status)
    

class PetsSchema(Schema):
    id = fields.Int(dump_only=True)
    pet_name = fields.Str()
    animal_type = fields.Nested(AnimalSchema(only=("animal",)), validate=must_not_be_blank)
    primary_breed = fields.Nested(BreedSchema(only=("breed",)), validate=must_not_be_blank)
    secondary_breed = fields.Nested(BreedSchema(only=("breed",)), validate=must_not_be_blank)
    gender = fields.Nested(GenderSchema(only=("gender",)), validate=must_not_be_blank)
    altered_status = fields.Nested(AlteredSchema(only=("status",)), validate=must_not_be_blank)
    pet_status = fields.Nested(PetStatusSchema(only=("status",)), validate=must_not_be_blank)
    trapper_id = fields.Str()
    date_created = fields.Str()
    format_pet= fields.Method("format_pet", dump_only=True)

    def format_pet(self, pets):
        return "{}, {}, {}, {}, {}, {}, {}, {}".format(Pets.pet_name, Pets.animal_type, Pets.primary_breed, 
        Pets.secondary_breed, Pets.gender, Pets.altered_status, Pets.trapper_id, Pets.date_created)

