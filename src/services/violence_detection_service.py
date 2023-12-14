import cv2
import keras
from ultralytics import YOLO
import numpy as np


lstm_model = keras.models.load_model('model\\best\\model.keras')
yolo_model = YOLO('model\\best\\yolov8n-pose.pt')

steps = 0
lst_of_dct = {'key_1':[],'key_2':[]}
label = " "
lst = []
predictions_lst = []
label_ = ''

LABELS = ["2-hands punch", "1-hand punch", "Standing", "Holding"] 


class ViolenceDetectionService:
    def __init__(self):
        pass
    def detect(self,image):
        global steps, lst_of_dct, label, lst, predictions_lst, label_
        minn = 1500
        points = {}
        i = 0
        label_ = ''

        results = yolo_model.predict(source=image, conf=0.60, classes=0, save=False)

        boxes = results[0].boxes
        result_keypoint = results[0].keypoints

        image = cv2.putText(image, f"there is {len(result_keypoint)}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        if len(result_keypoint[0].xy[0]) != 0:

            if len(result_keypoint) > 1:
                key1 = 0
                key2 = 0

                for box in boxes:

                    coordinates = box.xyxy[0]

                    x_c = (coordinates[0] + coordinates[2]) // 2
                    y_c = (coordinates[1] + coordinates[3]) // 2
                    p = (x_c, y_c)

                    points[i] = [coordinates, p]

                    for k in points.keys():
                        if i != k:
                            dis = ((points[i][1][0] - points[k][1][0]) ** 2 +
                                (points[i][1][1] - points[k][1][1]) ** 2) ** 0.5

                            if dis < minn:
                                minn = dis
                                key1 = i
                                key2 = k
                            
                    i += 1
                if key1 == 0 and key2 == 0:
                    keys = []
                else:
                    keys = [key1, key2]
            
                for z in range(len(keys)):

                    num = result_keypoint[keys[z]].xy[0].cpu().numpy()
                    num = num.reshape((1, 34))
                
                    if z == 0:
                        lst_of_dct['key_1'].append(num)
                        steps += 1
                    if z == 1:
                        lst_of_dct['key_2'].append(num)

                    if steps == 64:

                        if z == 0:
                            lst=lst_of_dct['key_1']
                        if z == 1:
                            lst=lst_of_dct['key_2']
                            steps = 0
                            lst_of_dct = {'key_1':[],'key_2':[]}

                        lst = np.array(lst)
                        lst = lst.reshape((1, 64, 34))
                        
                        preds = lstm_model.predict(lst)
                    

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
                    
                    # else:
                    #     label_="proccessing"
        image = cv2.putText(image, label_, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        return image