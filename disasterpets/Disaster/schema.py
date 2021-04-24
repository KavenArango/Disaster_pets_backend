from marshmallow import Schema, fields, ValidationError, pre_load, post_load, pre_dump
from disasterpets import ma
from disasterpets.Disaster.models import Disaster, DisasterLocationJoin, DisasterPetJoin

#fill in when we need disasters in pets tables
# Need <- relationships set up for pets and disaster to grab all info
class DisasterPetJoinSchema(ma.Schema):
	class Meta:
		model = DisasterPetJoin
		fields = ("id", "petid", "disasterid")


class DisasterLocationJoinSchema(ma.Schema):
	class Meta:
		model = DisasterLocationJoin
		include_fk = True
	id = ma.Function(lambda obj: obj.id)
	dis_id = ma.Function(lambda obj: obj.dis.id)
	local_id = ma.Function(lambda obj: obj.county.id)
	disaster_name = ma.Function(lambda obj: obj.dis.disaster_name)
	start_date = ma.Function(lambda obj: obj.dis.start_date)
	end_date = ma.Function(lambda obj: obj.dis.end_date)
	county = ma.Function(lambda obj: obj.county.countyname)
	state = ma.Function(lambda obj: obj.county.state)
	fields = ("id", "disaster_id", "location_id", "disaster_name", "start_date", "end_date", "county", "state")

#Not sure if well need a plain disaster schema may cut it 
class DisasterSchema(ma.Schema):
	class Meta:
		model = Disaster
		fields = ("id", "disaster_name", "start_date", "end_date")



