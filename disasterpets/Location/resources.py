from disasterpets.Location.models import CountyTable
from disasterpets import db
import datetime
from flask_restful import Resource
import json as simplejson
from flask import Flask, Blueprint, json, jsonify, request, make_response, current_app, url_for
from disasterpets.Location.schema import CountyTableSchema



def collectOneCounty(requestedData):
	countyschema = CountyTableSchema(many = True)
	county = CountyTable.query.filter(requestedData['id'] == CountyTable.id)
	result = countyschema.dump(county)
	return result

def collectAllCounties():
    countyschema = CountyTableSchema(many = True)
    counties = CountyTable.query.filter().all()
    results = countyschema.dump(counties)
    return results


def editCounty(requestedData):
	editcounty = CountyTable.query.filter(requestedData['id'] == CountyTable.id).first()
	CountyTable.countyname = requestedData['countyname']
	CountyTable.state = requestedData['state']
	db.session.commit()


def removeCounty(requestedData):
	allcounties = CountyTable.query.filter(requestedData['id'] == CountyTable.id).all()
	if requestedData['id'] in allcounties:
		CountyTable.query.filter(requestedData['id'] == CountyTable.id).delete()
		db.session.commit()
                
    
def addCounty(requestedData):
	newcounty = CountyTable(
		countyname = requestedData['countyname'],
		state = requestedData['state']
	)
	db.session.add(newcounty)
	db.session.commit()

class CountyManagerAPI(Resource):
    def patch(self): #edit disaster given id 
        try:
            requestedData = request.get_json()
            
            if bool(CountyTable.query.filter_by(id=requestedData['id']).first()):
                editCounty(requestedData)

                responseObject = {
                    'status': 'success',
                    'message': 'county updated'
                    }
                return make_response(jsonify(responseObject)), 201
            
            else:
                
                responseObject = {
                    'status': 'error',
                    'message': 'No counties found'
                    }
                return make_response(jsonify(responseObject)), 500
            
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404
    
    def post(self): #add a disaster
        try:
            requestedData = request.get_json()
            responseObject = {}
            if requestedData is None: 
                responseObject = {
                    'status': 'error',
                    'message': 'No data provided to add'
                    }
                return make_response(jsonify(responseObject)), 404
            else: 
                responseObject = {
                        'status': 'sucess',
                        'locations': addCounty(requestedData),
                        'message': 'County has been added'
                        }
                return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404
    def get(self): 
        try:
            responseObject = {
                    'status': 'sucess',
                    'locations': collectAllCounties(),
                    'message': 'all counties returned'
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'failed',
                'message': 'something went wrong try again'
            }
            return make_response(jsonify(responseObject)), 404