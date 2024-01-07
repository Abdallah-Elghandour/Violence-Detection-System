import unittest
import numpy as np
from unittest.mock import patch
from collections import namedtuple
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, ".."))
from src.services.violence_detection_service import ViolenceDetectionService  # Replace 'your_module' with the actual module name


class TestViolenceDetectionService(unittest.TestCase):
    def setUp(self):
        self.vd_service = ViolenceDetectionService()

    def test_calculate_distance(self):
            distance = self.vd_service.calculate_distance([0,(0, 0)], [0,(3, 4)])
            self.assertEqual(distance, 5)

    def test_centroid(self):
        centroid_point = self.vd_service.centroid(0, 0, 2, 4)
        self.assertEqual(centroid_point, (1, 2))

    def test_find_closest_points(self):
        Box = namedtuple('Box', ['xyxy'])
        boxes_data = [[3, 3, 5, 5], [1, 0, 5, 2], [0, 0, 2, 2], [0, 3, 2, 5]]
        boxes = [Box(xyxy=[data]) for data in boxes_data] 
        keys = self.vd_service.find_closest_points(boxes)
        self.assertEqual(keys, [2, 1])
              
    @patch('src.services.violence_detection_service.resend.Emails.send')
    def test_send_notification(self, mock_send):
        self.vd_service.send_notification()
        mock_send.assert_called_once_with({
            "from": "violence_detection_alert@resend.dev",
            "to": "abdullah456154@gmail.com",
            "subject": "Violence Detected Alert",
            "html": "<p><Strong>Violence</Strong> has been detected at the specified location.</p>"
        })

    @patch('src.services.violence_detection_service.logs_collection.insert_one')
    def test_add_log(self, mock_insert_one):
        self.vd_service.add_log()
        mock_insert_one.assert_called_once()

    def test_process_prediction(self):
        path = "unit test\\test_process_prediction.txt"
        def load_X(xPath):
            file = open(xPath, 'r')
            X_ = np.array(
                [elem for elem in [
                    row.split(',') for row in file
                ]], 
                dtype=np.float32
            )
            file.close()
            blocks = int(len(X_) / 64)
        
            X_ = np.array(np.split(X_,blocks))
            return X_ 
        lsts_of_keypoints = load_X(path)
        for lst_of_keypoints in lsts_of_keypoints:
            lst_of_keypoints = lst_of_keypoints.reshape((1, 64, 34))
            self.vd_service.process_prediction(lst_of_keypoints)

            
if __name__ == '__main__':
    unittest.main()

