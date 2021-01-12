from flask import Flask, Blueprint
from disasterpets.Pictures.resources import PetGalleryAPI

petgallerybp = Blueprint('petgallerybp', __name__)

petgallery_view = PetGalleryAPI.as_view('petgallery_api')

petgallerybp.add_url_rule(
    '/petgallery',
    view_func= petgallery_view,
    methods=['GET']
)