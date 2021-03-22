from disasterpets.Disaster.models import Disaster, DisasterLocationJoin, DisasterPetJoin
from disasterpets.Location.models import CountyTable
from disasterpets import db
import datetime
from flask_restful import Resource
import json as simplejson
from flask import Flask, Blueprint, json, jsonify, request, make_response, current_app, url_for
from disasterpets.Disaster.schema import DisasterLocationJoinSchema




def collectOneDisaster(requestedData):
    disasterlocationjoinschema = DisasterLocationJoinSchema(many = True)
    oneDisaster = DisasterLocationJoin.query.filter(requestedData['dis_id'] == DisasterLocationJoin.disasterid)
    onedisasterresults = disasterlocationjoinschema.dump(oneDisaster)
    return onedisasterresults

def collectAllDisasters():
    disasterlocationjoinschema = DisasterLocationJoinSchema(many = True)
    disLocIDS = DisasterLocationJoin.query.filter().all()
    disasterresults = disasterlocationjoinschema.dump(disLocIDS)

    return disasterresults



def editDisaster(requestedData):
    oneDisaster = Disaster.query.filter(requestedData['dis_id'] == Disaster.id).first()
    oneDisaster.disaster_name = requestedData['disaster_name']
    oneDisaster.start_date = requestedData['start_date']
    oneDisaster.end_date = requestedData['end_date']
    db.session.commit()

def addDisasterLocations(requestedData):
    alllocations = DisasterLocationJoin.query.filter(requestedData['dis_id'] == DisasterLocationJoin.disasterid).all()
    if requestedData["addloc"]:
        for location in requestedData["addloc"]:
            if requestedData["addloc"] not in alllocations:
                disasterlocation = DisasterLocationJoin(
                    disasterid = requestedData['dis_id'],
                    dlocationid = location
                )
                db.session.add(disasterlocation)
                db.session.commit()

def removeDisasterLocations(requestedData):
    alllocations = DisasterLocationJoin.query.filter(requestedData['dis_id'] == DisasterLocationJoin.disasterid).all()
    if requestedData["removeloc"]:
        for location in requestedData["removeloc"]:
            if requestedData["addloc"] in alllocations:
                DisasterLocationJoin.query.filter_by(
                    disasterid=requestedData['dis_id'], dlocationid=location).delete()
                db.session.commit()
                
    
def addDisaster(requestedData):

    newdisaster = Disaster(
        disaster_name = requestedData['disaster_name'],
        start_date = requestedData['start_date'],
        end_date = requestedData['end_date']
    )
    db.session.add(newdisaster)
    db.session.commit()

    locations = []
    for locid in requestedData['local_id']:
        db.session.refresh(newdisaster)
        disasterlocation = DisasterLocationJoin(
            disasterid = newdisaster.id,
            dlocationid = locid
        )
        db.session.add(disasterlocation)
        db.session.commit()

        locations.append(locid)
    return locations




class ManageDisasterAPI(Resource):
    def patch(self): 
        try:
            requestedData = request.get_json()
            
            if bool(DisasterLocationJoin.query.filter_by(id=requestedData['id']).first()):
                editDisaster(requestedData)
                addDisasterLocations(requestedData)
                removeDisasterLocations(requestedData)

                responseObject = {
                    'status': 'success',
                    'message': 'disaster updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No users found'
                    }
                return make_response(jsonify(responseObject)), 500
            
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404
    
    def post(self): 
        try:
            requestedData = request.get_json()
            responseObject = {}
            if requestedData is None: 
                responseObject = {
                    'status': 'error',
                    'message': 'No data provided to add'
                    }
                return make_response(jsonify(responseObject)), 404
            else if 'disaster_name' in requestedData:
                responseObject = {
                            'status': 'sucess',
                            'locations': addDisaster(requestedData),
                            'message': 'County has been added'
                        }
                return make_response(jsonify(responseObject)), 200
            else: 
                responseObject = {
                        'status': 'sucess',
                        'locations': collectOneDisaster(requestedData),
                        'message': 'Disaster has been added'
                        }
                return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404
    def get(self): #gets all disasters
        try:
            responseObject = {
                    'status': 'sucess',
                    'Disasters': collectAllDisasters(),
                    'message': 'all disasters returned'
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404







