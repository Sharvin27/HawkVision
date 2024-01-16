from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import pytesseract
import pyttsx3

@gzip.gzip_page
def live(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'live.html')

#to capture video class
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        # Create a TTS engine
        self.engine = pyttsx3.init()

        # Set up Tesseract OCR
        pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        # Convert the frame to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Perform text detection using Tesseract OCR
        detected_text = pytesseract.image_to_string(gray)

        # Remove leading/trailing whitespaces and filter out empty lines
        detected_text = '\n'.join(line.strip() for line in detected_text.split('\n') if line.strip())
        print(detected_text)

        self.engine.say(detected_text)
        self.engine.runAndWait()

        _, jpeg = cv2.imencode('.jpg', gray)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')