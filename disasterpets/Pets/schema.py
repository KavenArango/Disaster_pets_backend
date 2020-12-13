from marshmallow import Schema, fields, ValidationError, pre_load

class PetsSchema(Schema):
    id = fields.Int(dump_only=True)
    pet_name = fields.Str()
    animal_type = fields.Str()
    primary_breed = fields.Str()
    secondary_breed = fields.Str()
    gender = fields.Str()
    altered_status = fields.Str()
    trapper_id = fields.Str()
    date_created = fields.Str()
    format_pet= fields.Method("format_pet", dump_only=True)

    def format_pet(self, pets):
        return "{}, {}, {}, {}, {}, {}, {}, {}".format(Pets.pet_name, Pets.animal_type, Pets.primary_breed, 
        Pets.secondary_breed, Pets.gender, Pets.altered_status, Pets.trapper_id, Pets.date_created)