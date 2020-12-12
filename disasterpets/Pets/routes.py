from flask import Flask, Blueprint
from disasterpets.Pets.resources import AddPetAPI, UploadImageAPI

petbp = Blueprint('petbp', __name__)

addpet_view = AddPetAPI.as_view('addpet_api')
upload_image = UploadImageAPI.as_view('uploadimage_api')

petbp.add_url_rule(
    '/addpet',
    view_func= addpet_view,
    methods=['POST']
)
petbp.add_url_rule(
    '/uploadimage',
    view_func= upload_image,
    methods=['POST']
)