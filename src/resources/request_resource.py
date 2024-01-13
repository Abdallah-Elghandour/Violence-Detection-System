from src.resources.base_resource import BaseResource
from src.services.request_service import RequestService

#this class is responsible for the request resource
class RequestResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.__request_service = RequestService()

    def post(self):
        return self.__request_service.tasks()
    