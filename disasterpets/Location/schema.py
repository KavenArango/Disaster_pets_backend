from marshmallow import Schema, fields, ValidationError, pre_load, post_load, pre_dump
from disasterpets import ma
from disasterpets.Location.models import CountyTable

class CountyTableSchema(ma.Schema):
	class Meta:
		model = CountyTable
		fields = ("id", "countyname", "state")