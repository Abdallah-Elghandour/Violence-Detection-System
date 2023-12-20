import cv2
import keras
from ultralytics import YOLO
import numpy as np


lstm_model = keras.models.load_model('model\\best\\model.keras')
yolo_model = YOLO('model\\best\\yolov8n-pose.pt')

steps = 0
lst_of_dct = {'key_1':[],'key_2':[]}
predictions_lst = []
label_ = ''

LABELS = ["2-hands punch", "1-hand punch", "Standing", "Holding"] 


class ViolenceDetectionService:
    def __init__(self):
        pass
    def detect(self,image):
        global label_
        
        label_ = ''

        results = yolo_model.predict(source=image, conf=0.60, classes=0, save=False)

        boxes = results[0].boxes
        result_keypoint = results[0].keypoints

        image = cv2.putText(image, f"there is {len(result_keypoint)}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        if len(result_keypoint[0].xy[0]) != 0:

            if len(result_keypoint) > 1:
                keys = self.find_closest_points(boxes)
                self.proccess_keypoints(result_keypoint, keys)
                
        image = cv2.putText(image, label_, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        return image
    
    def find_closest_points(self, boxes):
        key1 = 0
        key2 = 0
        minn = 1500
        points = {}

        for i, box in enumerate(boxes):

            coordinates = box.xyxy[0]

            
            centroid_point = self.centroid(coordinates[0], coordinates[1], coordinates[2], coordinates[3])

            points[i] = [coordinates, centroid_point]

            for j in points.keys():
                if i != j:
                    distance = self.calculate_distance(points[i], points[j])

                    if distance < minn:
                        minn = distance
                        key1 = i
                        key2 = j
                    
        if key1 == 0 and key2 == 0:
            keys = []
        else:
            keys = [key1, key2]

        return keys
    
    def calculate_distance(self, point1, point2):
        return ((point1[1][0] - point2[1][0]) ** 2 +
                        (point1[1][1] - point2[1][1]) ** 2) ** 0.5
    
    def centroid(self, x1, y1, x2, y2):
        return ((x1 + x2) // 2, (y1 + y2) // 2)
    
    def proccess_keypoints(self, keypoints, keys):
        global steps, lst_of_dct
        for i in range(len(keys)):

                    num = keypoints[keys[i]].xy[0].cpu().numpy()
                    num = num.reshape((1, 34))
                
                    if i == 0:
                        lst_of_dct['key_1'].append(num)
                        steps += 1
                    if i == 1:
                        lst_of_dct['key_2'].append(num)

                    if steps == 64:

                        if i == 0:
                            lst_of_keypoints = lst_of_dct['key_1']
                        if i == 1:
                            lst_of_keypoints = lst_of_dct['key_2']
                            steps = 0
                            lst_of_dct = {'key_1':[],'key_2':[]}

                        lst_of_keypoints = np.array(lst_of_keypoints)
                        lst_of_keypoints = lst_of_keypoints.reshape((1, 64, 34))
                        self.process_prediction(lst_of_keypoints)
                        
                        
    def process_prediction(self, lst_of_keypoints):
        global predictions_lst, label_

        preds = lstm_model.predict(lst_of_keypoints)
                    
        threshold = 0.8
        predicted_probabilities = preds[0]

        max_prob = np.max(predicted_probabilities)

        if max_prob > threshold:
            
            label = LABELS[np.argmax(preds)]
            predictions_lst.append(label)
        else:
            label = "NORMAL"
            predictions_lst.append(label)
        
        lst = []
        if len(predictions_lst) == 6:
            
            if (predictions_lst.count('2-hands punch') + predictions_lst.count('1-hand punch')) >= 4:
                label_ = "Violence"
            else:
                label_ = "No Violence"
            predictions_lst=[]