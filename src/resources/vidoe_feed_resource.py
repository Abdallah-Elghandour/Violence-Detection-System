from src.resources.base_resource import BaseResource
from src.services.video_feed_service import VideoFeedService
from flask import Response

class VideoFeedResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.__video_feed_service = VideoFeedService()
    def get(self):
        return Response(self.__video_feed_service.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')