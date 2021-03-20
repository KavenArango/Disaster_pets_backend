from flask import Flask, Blueprint, jsonify, request, make_response, current_app
from disasterpets.Account.models import User
from disasterpets import db, bcrypt, mail, url
from flask.views import MethodView
import jwt
import datetime


from disasterpets.Disaster.resources import (
	ManageDisasterAPI,
)


disastermanger = Blueprint("disastermanger", __name__)

managedisaster_view = ManageDisasterAPI.as_view("managedisaster_api")

disastermanger.add_url_rule(
    '/managedisater',
    view_func= managedisaster_view,
    methods=['POST', 'PATCH', 'GET']
)