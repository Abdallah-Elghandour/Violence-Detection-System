from src.resources.violence_detection_resource import ViolenceDetectionResource
from src.resources.vidoe_feed_resource import VideoFeedResource
from src.resources.request_resource import RequestResource

# this file is responsible for the routes of the application

def violence_detection_route(api):
    api.add_resource(ViolenceDetectionResource, "/")

def requests_route(api):
    api.add_resource(RequestResource, '/request', endpoint="tasks")

def video_feed_route(api):
    api.add_resource(VideoFeedResource, '/video', endpoint="video_feed")