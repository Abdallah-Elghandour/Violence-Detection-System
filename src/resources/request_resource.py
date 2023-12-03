from src.resources.base_resource import BaseResource
from src.services.request_service import RequestService


class RequestResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.__request_service = RequestService()

    def post(self):
        return self.__request_service.tasks()
    
    # def get(self):
    #     return  self.__request_service.tasks()