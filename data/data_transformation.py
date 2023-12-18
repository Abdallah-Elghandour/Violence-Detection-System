from ultralytics import YOLO
import numpy as np
import cv2
import os


path = "D:\\Final Project\\Violence Detection\\dataset2\\videos\\standing\\"
filenames = os.listdir(path)

yolo_model = YOLO('models\\yolov8n-pose.pt')

fileX = open("dataset2\\64 frames data\\X_Standing.txt", 'a')
fileY = open("dataset2\\64 frames data\\Y_Standing.txt", "a") 


for filename in filenames:

    lst_of_dict = {"person1":[]}
    frames_count = 0
    # person1_counter = 0
    # person2_counter = 0
    line = ""

    cap = cv2.VideoCapture(path + filename)

   
    while True:
        success, frame = cap.read()
        
        
        if success:
            # frame = cv2.resize(frame, (640, 480))
            
            results = yolo_model.predict(source=frame, conf=0.70, classes=0, save=False, boxes=False, show_labels=False, show_conf=False)

            result_keypoints = results[0].keypoints

            if len(result_keypoints) != 1:
                continue
            # for i in range(1):
            person_keypoints = result_keypoints[0].xy[0].cpu().numpy()
            
            if len(person_keypoints) == 0:
                break
            person_keypoints = person_keypoints.reshape((1, 34))

            # if i == 0:
            lst_of_dict["person1"].append(person_keypoints)
            frames_count += 1
                # person1_counter +=1
            # if i == 1:
            #     lst_of_dict["person2"].append(person_keypoints)
                # person2_counter +=1

            if frames_count == 64:
                # if i == 0:
                for keypoint in lst_of_dict["person1"]:
                    for key in keypoint[0]:
                        line = line + "%.3f," % key

                    line = line[:-1] + "\n"
                    fileX.write(line)
                    line = ""

                fileY.write("2\n")
                # frames_count = 0
                # lst_of_dict = {"person1": []}
                break
                    # person1_counter = 0
                    # lst_of_dict = {"person1": [], "person2": lst_of_dict["person2"]}
            
                    # if i == 1:
                    #     for keypoint in lst_of_dict["person2"]:
                    #         for key in keypoint[0]:
                    #             line = line + "%.3f," % key

                    #         line = line[:-1] + "\n"
                    #         fileX.write(line)
                    #         line = ""

                    #     fileY.write("0\n")
                    #     # person2_counter = 0    
                
                    #     lst_of_dict = {"person1": [], "person2":[]}
            # else: 
                # fileMistakes.write(f"one person detected or more than 2 perosn file name: {filename}\n")
        else: 
            break


fileX.close()
fileY.close()

