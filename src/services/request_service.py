from flask import request, render_template, Response
import cv2

class RequestService:
    
    switch = False
    cap = cv2.VideoCapture("http://192.168.1.72:8080/video")

    def __init__(self):
        pass
    def tasks(self):
    
        if request.method == 'POST':
            if request.form.get('start') == 'Start':
                RequestService.switch = True
                RequestService.cap = cv2.VideoCapture("http://192.168.1.72:8080/video")

            elif request.form.get('stop') == 'Stop':
                
                if RequestService.switch:
                    RequestService.cap.release()
                    cv2.destroyAllWindows()
                    RequestService.switch = False

        return Response(render_template('index.html', switch=RequestService.switch)) 