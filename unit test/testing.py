# import unittest
# import cv2
# import numpy as np
# from unittest.mock import patch, MagicMock
# from src.services.violence_detection_service import ViolenceDetectionService  # Replace 'your_module' with the actual module name
# from collections import namedtuple
# import torch
# class TestViolenceDetectionService(unittest.TestCase):
#     def setUp(self):
#         self.vd_service = ViolenceDetectionService()

#     # def test_calculate_distance(self):
#     #         distance = self.vd_service.calculate_distance([0,(0, 0)], [0,(3, 4)])
#     #         self.assertEqual(distance, 5)

#     # def test_centroid(self):
#     #     centroid_point = self.vd_service.centroid(0, 0, 2, 4)
#     #     self.assertEqual(centroid_point, (1, 2))

#     # def test_find_closest_points(self):
#     #     Box = namedtuple('Box', ['xyxy'])
#     #     boxes_data = [[3, 3, 5, 5], [1, 0, 5, 2], [0, 0, 2, 2], [0, 3, 2, 5]]
#     #     boxes = [Box(xyxy=[data]) for data in boxes_data] 
#     #     keys = self.vd_service.find_closest_points(boxes)
#     #     self.assertEqual(keys, [2, 1])
              
#     # @patch('src.services.violence_detection_service.resend.Emails.send')
#     # def test_send_notification(self, mock_send):
#     #     self.vd_service.send_notification()
#     #     mock_send.assert_called_once_with({
#     #         "from": "violence_detection_alert@resend.dev",
#     #         "to": "abdullah456154@gmail.com",
#     #         "subject": "Violence Detected Alert",
#     #         "html": "<p><Strong>Violence</Strong> has been detected at the specified location.</p>"
#     #     })

#     # @patch('src.services.violence_detection_service.logs_collection.insert_one')
#     # def test_add_log(self, mock_insert_one):
#     #     self.vd_service.add_log()
#     #     mock_insert_one.assert_called_once()

#     # def test_process_prediction(self):
#     #     path = "test_process_prediction.txt"
#     #     def load_X(xPath):
#     #         file = open(xPath, 'r')
#     #         X_ = np.array(
#     #             [elem for elem in [
#     #                 row.split(',') for row in file
#     #             ]], 
#     #             dtype=np.float32
#     #         )
#     #         file.close()
#     #         blocks = int(len(X_) / 64)
        
#     #         X_ = np.array(np.split(X_,blocks))
#     #         return X_ 
#     #     lsts_of_keypoints = load_X(path)
#     #     for lst_of_keypoints in lsts_of_keypoints:
#     #         lst_of_keypoints = lst_of_keypoints.reshape((1, 64, 34))
#     #         self.vd_service.process_prediction(lst_of_keypoints)
#     def test_process_keypoints(self):
#         path = "test_process_keypoints.txt"
#         def load_X(xPath):
#             file = open(xPath, 'r')
#             X_ = np.array(
#                 [elem for elem in [
#                     row.split(',') for row in file
#                 ]], 
#                 dtype=np.float32
#             )
#             file.close()
#             blocks = int(len(X_) / 64)
            
#             X_ = np.array(np.split(X_,blocks))

#             return X_ 

#         load = load_X(path)
#         load = load.reshape((2, 64, 17, 2))
#         person1 = load[0]
#         person2 = load[1]

#         Keypoint = namedtuple('Keypoint', ['xy'])

#         for i in range(64):
#             keypoint_struct =[]
#             keypoint_struct.append(Keypoint(xy=[person1[i]]))
#             keypoint_struct.append(Keypoint(xy=[person2[i]]))
#             keypoint_struct = np.array(keypoint_struct)
#             keypoints = torch.from_numpy(keypoint_struct)
            
#             self.vd_service.process_keypoints(keypoints, [0, 1])

            
# if __name__ == '__main__':
#     unittest.main()



import unittest
from unittest.mock import MagicMock
from flask import Response
from src.services.request_service import RequestService  # replace with the actual module containing RequestService
import app
class TestRequestService(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.request_service = RequestService()

    def test_tasks_start(self):
        with self.app:
            mock_request = MagicMock()
            mock_request.method = 'POST'
            mock_request.form.get.return_value = 'Start'

            with unittest.mock.patch('your_flask_app.request', mock_request):
                response = self.request_service.tasks()

            self.assertTrue(RequestService.switch)
            self.assertIsInstance(response, Response)
            # Add more assertions if needed

    def test_tasks_stop(self):
        with self.app:
            RequestService.switch = True  # Simulate that the switch is already on
            mock_request = MagicMock()
            mock_request.method = 'POST'
            mock_request.form.get.return_value = 'Stop'

            with unittest.mock.patch('your_flask_app.request', mock_request):
                response = self.request_service.tasks()

            self.assertFalse(RequestService.switch)
            self.assertIsInstance(response, Response)
            # Add more assertions if needed

    def test_tasks_exception_handling(self):
        with self.app:
            mock_request = MagicMock()
            mock_request.method = 'POST'
            mock_request.form.get.side_effect = Exception("Simulated error")

            with unittest.mock.patch('your_flask_app.request', mock_request):
                response = self.request_service.tasks()

            self.assertFalse(RequestService.switch)
            self.assertIsInstance(response, Response)
            # Add more assertions if needed

if __name__ == '__main__':
    unittest.main()
