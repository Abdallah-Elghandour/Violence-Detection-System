import cv2
from src.services.request_service import RequestService
from src.services.violence_detection_service import ViolenceDetectionService


class VideoFeedService:
    def __init__(self):
        self._request = RequestService()
        self._detect = ViolenceDetectionService()
    def generate_frames(self):
        try:

            if self._request.switch:

                while True:
                    success, frame = self._request.cap.read()
                    if success:
                        frame = self._detect.detect(frame)
                        try:
                            ret, buffer = cv2.imencode('.jpg', frame)
                            frame = buffer.tobytes()
                            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                        except Exception as e:
                            pass
        except Exception as e:
            print(f"Error during generate_frames: {e}")