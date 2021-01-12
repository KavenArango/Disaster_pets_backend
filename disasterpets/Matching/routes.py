from flask import Flask, Blueprint
from disasterpets.Matching.resources import PetMatchAPI

matchingbp = Blueprint('matchingbp', __name__)

matching_view = PetMatchAPI.as_view('petmatch_api')

matchingbp.add_url_rule(
    '/petmatching',
    view_func= matching_view,
    methods=['GET']
)