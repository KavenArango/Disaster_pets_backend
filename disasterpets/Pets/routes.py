from flask import Flask, Blueprint
from disasterpets.Pets.resources import AddPetAPI, UploadImageAPI, PetDetailAPI

petbp = Blueprint('petbp', __name__)

addpet_view = AddPetAPI.as_view('addpet_api')
upload_image = UploadImageAPI.as_view('uploadimage_api')
pet_detail = PetDetailAPI.as_view('petdetail_api')

petbp.add_url_rule(
    '/addpet',
    view_func= addpet_view,
    methods=['POST', 'GET']
)
petbp.add_url_rule(
    '/uploadimage',
    view_func= upload_image,
    methods=['POST']
)

petbp.add_url_rule(
    '/petdetails',
    view_func= pet_detail,
    methods = ['GET']
)