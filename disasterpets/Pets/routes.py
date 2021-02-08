from flask import Flask, Blueprint
from disasterpets.Pets.resources import AddPetAPI, UploadImageAPI, PetDetailAPI, ManagePetAPI, ManageAlteredStatAPI, ManageAnimalTypeAPI

petbp = Blueprint('petbp', __name__)

addpet_view = AddPetAPI.as_view('addpet_api')
upload_image = UploadImageAPI.as_view('uploadimage_api')
pet_detail = PetDetailAPI.as_view('petdetail_api')
managepet_view = ManagePetAPI.as_view('managepet_api')
managealteredstatus_view = ManageAlteredStatAPI.as_view('managealteredstatus_api')
manageanimaltype_view = ManageAnimalTypeAPI.as_view('manageanimaltype_api')


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
    methods = ['POST']
)



petbp.add_url_rule(
    '/managepets',
    view_func= managepet_view,
    methods=['POST', 'GET']
)



petbp.add_url_rule(
    '/managealteredstatus',
    view_func= managealteredstatus_view,
    methods=['POST', 'PATCH', 'GET']
)



petbp.add_url_rule(
    '/manageanimaltype',
    view_func= manageanimaltype_view,
    methods=['POST', 'PATCH', 'GET']
)