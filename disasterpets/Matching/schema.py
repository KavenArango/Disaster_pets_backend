from marshmallow import Schema, fields, ValidationError, pre_load, post_load, pre_dump
from disasterpets import ma
from disasterpets.Matching.models import(
    PotentialMatch,
    PotentialMatchJoin,
    RejectMatch,
    RejectMatchJoin,
)


class PotentialMatchSchema(ma.Schema):
    class Meta:
        model = PotentialMatch
        fields = ('id', 'petid', 'admincheck')


class PotentialMatchJoinSchema(ma.Schema):
    class Meta:
        model = PotentialMatchJoin
        fields = ('petid', 'potentialid', 'admincheck')
