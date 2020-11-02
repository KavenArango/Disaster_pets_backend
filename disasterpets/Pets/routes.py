from flask import Flask, Blueprint
from disasterpets.Pets.resources import AddPetAPI

petbp = Blueprint('petbp', __name__)

addpet_view = AddPetAPI.as_view('addpet_api')

petbp.add_url_rule(
    '/addpet',
    view_func= addpet_view,
    methods=['POST']
)
        