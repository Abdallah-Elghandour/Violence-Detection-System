from flask import Flask, render_template, Response, request
import cv2
import keras
from ultralytics import YOLO
from config import Config
import numpy as np


switch = False
steps = 0
lst_of_dct = {'key_1':[],'key_2':[]}
label = " "
lst = []
predictions_lst = []
label_ = ''

LABELS = [    
    "JUMPING",
    "JUMPING_JACKS",
    "BOXING",
    "WAVING_2HANDS",
    "WAVING_1HAND",
    "CLAPPING_HANDS"
] 

lstm_model = keras.models.load_model('models\\model.keras')
yolo_model = YOLO('yolov8n-pose.pt')



app = Flask(__name__, template_folder='src/templates')



def detect(image):
    global steps, lst_of_dct, label, lst, predictions_lst, label_
    minn = 1500
    points = {}
    i = 0

    results = yolo_model.predict(source=image, conf=0.60, classes=0, save=False)

    boxes = results[0].boxes
    result_keypoint = results[0].keypoints

    image = cv2.putText(cv2.flip(image,1), f"there is {len(result_keypoint)}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
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

            if steps == 32:

                if z == 0:
                    lst=lst_of_dct['key_1']
                if z == 1:
                    lst=lst_of_dct['key_2']
                    steps = 0
                    lst_of_dct = {'key_1':[],'key_2':[]}

                lst = np.array(lst)
                lst = lst.reshape((1, 32, 34))
                
                preds = lstm_model.predict(lst)
               

                threshold = 0.94
                predicted_probabilities = preds[0]

                max_prob = np.max(predicted_probabilities)

                if max_prob > threshold:
                    
                    label = LABELS[np.argmax(preds)]
                    predictions_lst.append(label)
                else:
                    label = "NORMAL"
                    predictions_lst.append(label)
                
                lst = []
            if len(predictions_lst) == 8:
                
                if predictions_lst.count('BOXING')>=4:
                    label_ = "Violence"
                else:
                    label_ = "No Violence"
                predictions_lst=[]
               
            # else:
            #     label_="proccessing"
    image = cv2.putText(cv2.flip(image,1), label_, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    image = cv2.flip(image,1)
    return image


def generate_frames():
 
    while True:
        success, frame = cap.read()
        if success:
            frame = detect(frame)
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests', methods=['POST', 'GET'])
def tasks():
    global switch, cap
    if request.method == 'POST':
        if request.form.get('start') == 'Start':
            switch = True
            cap = cv2.VideoCapture(0)

        elif request.form.get('stop') == 'Stop':
            if switch:
                cap.release()
                cv2.destroyAllWindows()
                switch = False

    return render_template('index.html')



if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)