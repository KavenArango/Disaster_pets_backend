from flask import Flask, Blueprint
from disasterpets.Pictures.resources import PetGalleryAPI, RainbowGalleryAPI

petgallerybp = Blueprint('petgallerybp', __name__)
rainbowgallerybp = Blueprint('rainbowgallerybp', __name__)

petgallery_view = PetGalleryAPI.as_view('petgallery_api')
rainbowgallery_view = RainbowGalleryAPI.as_view('rainbowgallery_api')

petgallerybp.add_url_rule(
    '/petgallery',
    view_func= petgallery_view,
    methods=['GET']
)

rainbowgallerybp.add_url_rule(
    '/rainbowgallery',
    view_func= rainbowgallery_view,
    methods=['GET']
)