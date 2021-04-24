from flask import Flask, Blueprint, jsonify, request, make_response, current_app
from disasterpets.Account.models import User
from disasterpets import db, bcrypt, mail, url
from flask.views import MethodView
import jwt
import datetime


from disasterpets.Location.resources import (
	CountyManagerAPI,
)


countymanger = Blueprint("countymanger", __name__)

countymanager_view = CountyManagerAPI.as_view("countymanager_api")

countymanger.add_url_rule(
    '/countymanager',
    view_func= countymanager_view,
    methods=['POST', 'PATCH', 'GET']
)