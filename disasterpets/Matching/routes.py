from flask import Flask, Blueprint
from disasterpets.Matching.resources import PetMatchAPI, ManageMatchAPI

matchingbp = Blueprint('matchingbp', __name__)

matching_view = PetMatchAPI.as_view('petmatch_api')
managepetmatch_view = ManageMatchAPI.as_view('managepetmatch_api')



matchingbp.add_url_rule(
    '/petmatching',
    view_func= matching_view,
    methods=['GET']
)


matchingbp.add_url_rule(
    '/managepetmatch',
    view_func= managepetmatch_view,
    methods=['POST', 'GET', 'PATCH']
)