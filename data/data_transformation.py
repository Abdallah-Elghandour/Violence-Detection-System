from ultralytics import YOLO
import cv2
import os

#in this file we transform our videos to data keypoints file

# **************add your videos path to transoform your data****************
# path = "Violence Detection\\dataset\\videos\\standing\\"
#************************************************************
current_directory = os.getcwd()
project_path= os.path.abspath(os.path.join(current_directory, "../.."))

filenames = os.listdir(path)
yolo_model = YOLO(f'{project_path}/model/best/yolov8n-pose.pt')

# files to write class keypoint data and class labels
fileX = open("data\\dataset\\X_Standing.txt", 'a')
fileY = open("data\\dataset\\Y_Standing.txt", 'a') 


for filename in filenames:

    lst_of_dict = {"person1":[]}
    frames_count = 0
    line = ""

    cap = cv2.VideoCapture(path + filename)

   
    while True:
        success, frame = cap.read()
        
        if success:
            
            results = yolo_model.predict(source=frame, conf=0.70, classes=0, save=False, boxes=False, show_labels=False, show_conf=False)

            result_keypoints = results[0].keypoints

            if len(result_keypoints) != 1:
                continue
            
            person_keypoints = result_keypoints[0].xy[0].cpu().numpy()
            
            if len(person_keypoints) == 0:
                break

            person_keypoints = person_keypoints.reshape((1, 34))
            lst_of_dict["person1"].append(person_keypoints)
            frames_count += 1

            if frames_count == 64:

                for keypoint in lst_of_dict["person1"]:
                    for key in keypoint[0]:
                        line = line + "%.3f," % key

                    line = line[:-1] + "\n"
                    fileX.write(line)
                    line = ""

                fileY.write("2\n") # write class number as label
                break
        else: 
            break


fileX.close()
fileY.close()

