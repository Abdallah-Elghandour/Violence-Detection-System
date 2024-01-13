from flask import Response, render_template
from src.resources.base_resource import BaseResource

# this class is responsible for the get main page resource
class ViolenceDetectionResource(BaseResource):
    def __init__(self):
        super().__init__()

    def get(self):
        return Response(render_template('index.html'))
