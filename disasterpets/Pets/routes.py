from flask import Flask, Blueprint
from disasterpets.Pets.resources import (
    AddPetAPI,
    UploadImageAPI,
    PetDetailAPI,
    ManagePetAPI,
    ManageAlteredStatAPI,
    ManageAnimalTypeAPI,
    ManageBreedsAPI,
    ManageGenderAPI,
    ManagePetStatusAPI,
    ManageUniqueFeaturesAPI,
    ManageFeaturesAPI,
    ManageColorsAPI,
    ManagePositionsAPI,
    ManageBodyPartsAPI,
    UniqueFeaturesInfoAPI,
    )

petbp = Blueprint('petbp', __name__)

addpet_view = AddPetAPI.as_view('addpet_api')
upload_image = UploadImageAPI.as_view('uploadimage_api')
pet_detail = PetDetailAPI.as_view('petdetail_api')
managepet_view = ManagePetAPI.as_view('managepet_api')
managealteredstatus_view = ManageAlteredStatAPI.as_view('managealteredstatus_api')
manageanimaltype_view = ManageAnimalTypeAPI.as_view('manageanimaltype_api')
managebreeds_view = ManageBreedsAPI.as_view('managebreeds_api')
managegender_view = ManageGenderAPI.as_view('managegender_api')
managepetstatus_view = ManagePetStatusAPI.as_view('managepetstatus_api')

manageuniquefeatures_view = ManageUniqueFeaturesAPI.as_view('manageuniquefeatures_api')
managefeatures_view = ManageFeaturesAPI.as_view('managefeatures_api')
managecolor_view = ManageColorsAPI.as_view('managecolor_api')
manageposition_view = ManagePositionsAPI.as_view('manageposition_api')
managebodypart_view = ManageBodyPartsAPI.as_view('managebodypart_api')
uniquefeaturesinfo_view = UniqueFeaturesInfoAPI.as_view('uniquefeaturesinfo_api') # STEVE WANTED THIS NAME



petbp.add_url_rule(
    '/uniquefeaturesinfo',
    view_func= uniquefeaturesinfo_view,
    methods=['GET']
)

petbp.add_url_rule(
    '/managefeatures',
    view_func= managefeatures_view,
    methods=['POST', 'PATCH', 'GET']
)

petbp.add_url_rule(
    '/managecolor',
    view_func= managecolor_view,
    methods=['POST', 'PATCH', 'GET']
)

petbp.add_url_rule(
    '/manageposition',
    view_func= manageposition_view,
    methods=['POST', 'PATCH', 'GET']
)

petbp.add_url_rule(
    '/managebodypart',
    view_func= managebodypart_view,
    methods=['POST', 'PATCH', 'GET']
)

petbp.add_url_rule(
    '/manageuniquefeatures',
    view_func= manageuniquefeatures_view,
    methods=['POST', 'PATCH', 'GET']
)

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
    methods=['PATCH', 'POST']
)

petbp.add_url_rule(
    '/managealteredstatus',
    view_func= managealteredstatus_view,
    methods=['POST', 'PATCH', 'GET']
)

petbp.add_url_rule(
    '/managebreeds',
    view_func= managebreeds_view,
    methods=['POST', 'PATCH', 'GET']
)

petbp.add_url_rule(
    '/managegender',
    view_func= managegender_view,
    methods=['POST', 'PATCH', 'GET']
)

petbp.add_url_rule(
    '/managepetstatus',
    view_func= managepetstatus_view,
    methods=['POST', 'PATCH', 'GET']
)

petbp.add_url_rule(
    '/manageanimaltype',
    view_func= manageanimaltype_view,
    methods=['POST', 'PATCH', 'GET']
)