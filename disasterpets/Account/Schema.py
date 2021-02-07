from marshmallow import Schema, fields, ValidationError, pre_load, post_load, pre_dump
from disasterpets import ma
from disasterpets.Account.models import User, Role, SocialMedia, ReporterInfo, ReporterInfoJoin


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = (
            "id",
            "fname",
            "lname",
            "email",
            "password",
            "phone",
            "phone2",
            "date_created",
            "last_logged",
            "role_id",
            "social",
        )


class RoleSchema(ma.Schema):
    class Meta:
        model = Role
        fields = ("id", "role_name")


class SocialMediaScheme(ma.Schema):
    class Meta:
        model = SocialMedia
        fields = (
            "id",
            "fname",
            "lname",
            "email",
            "password",
            "phone",
            "phone2",
            "date_created",
            "last_logged",
            "role_id",
            "social",
        )


class ReporterInfoSchema(ma.Schema):
    class Meta:
        model = ReporterInfo
        fields = ("id", "spottedlocation", "spottedimage", "userid", "notes")


class ReporterInfoJoinSchema(ma.Schema):
    class Meta:
        model = ReporterInfoJoin
        include_fk = True
    id = ma.Function(lambda obj: obj.id)
    fname = ma.Function(lambda obj: obj.fname)
    reporterid= ma.Function(lambda obj: obj.pbreed.breed)
    secondary_breed = ma.Function(lambda obj: obj.sbreed.breed)
    gender = ma.Function(lambda obj: obj.sex.gender)
    altered_status = ma.Function(lambda obj: obj.alteredstat.status)
    animal_type = ma.Function(lambda obj: obj.animal.animal)
    pet_status = ma.Function(lambda obj: obj.pet.pet_status)
    date_created = ma.Function(lambda obj: obj.date_created)
    trapper_id = ma.Function(lambda obj: obj.trapper_id)
    fields = ('id', 'pet_name', 'primary_breed', 'primary_bid', 'secondary_breed',
        'gender', 'animal_type', 'pet_status', 'altered_status', 'trapper_id', 'date_created')
