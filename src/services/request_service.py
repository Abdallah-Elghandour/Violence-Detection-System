import src.services.violence_detection_service as vds
from flask import request, render_template, Response
import cv2

#this class is responsible for the request service such as start and stop the video feed
class RequestService:
    switch = False
    cap = None

    def __init__(self):
        pass
    def tasks(self):
        
        try:
            if request.method == 'POST':
                if request.form.get('start') == 'Start':
                    RequestService.switch = True
                    RequestService.cap = cv2.VideoCapture("a.mp4")#http://192.168.1.72:8080/video   
                
                elif request.form.get('stop') == 'Stop':
                    
                    if RequestService.switch:
                        RequestService.cap.release()
                        cv2.destroyAllWindows()
                        RequestService.switch = False
                        vds.predictions_lst = []
                        vds.label_ = ''
                        vds.steps = 0
                        vds.lst_of_dct = {'key_1':[],'key_2':[]}
        except Exception as e:
            print(f"Error during tasks: {e}")
            
        return Response(render_template('index.html', switch=RequestService.switch))