from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)

############################################################## CAMERA

import cv2
import numpy as np
import dlib
import pandas as pd #pandas 1.0.3
import time
import datetime #pip install dateTime 4.3

sp = "var/www/webApp/webApp/shape_predictor_68_face_landmarks.dat"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(sp)

class VideoCamera:
    def __init__(self):
       #capturing video
        self.cap = getCam()
        #stackoverflowsaso con cap cuando es nulo
        self.prediction_points = []
    
    def __del__(self):
        #releasing camera
        self.cap.release()
    def get_frame(self):    

        _, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
        faces = detector(gray)

        x1_max = 0
        x2_max = 0
        y1_max = 0
        y2_max = 0

        max_area = returnArea(x1_max,x2_max,y1_max,y2_max)

        actual_face = [(None,None),(None,None)]
        for face in faces:
        
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            temp_area = returnArea(x1,x2,y1,y2)

            if max_area < temp_area:
                x1_max = x1
                x2_max = x2
                y1_max = y1
                y2_max = y2
                actual_face = face               
    
        #cv2.rectangle(frame,(x1_max,y1_max),(x2_max,y2_max),green,3)

        #Conseguir los 68 puntos del rostro predominante de este frame
        if len(faces) == 0:
            ret, jpeg = cv2.imencode('.jpg', frame)        
            return jpeg.tobytes(), 0
        else:
            landmarks = predictor(gray, actual_face)
            face_points = []

            for i in range(0, 68):       
                cv2.circle(frame, (landmarks.part(i).x,landmarks.part(i).y), 4, (255, 0, 0), -1)
                face_points.append((landmarks.part(i).x,landmarks.part(i).y))
            self.prediction_points.append(face_points)

        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)        
        return jpeg.tobytes(), 1

        if cam_initialized == False:
            cam_initialized = True
            time_start = time.time()

def returnArea(x1,x2,y1,y2):
    return (x2-x1) * (y2-y1)

def getCam():
    cap = cv2.VideoCapture(0)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source')
        return 0
    else:
        return cap

'''
#Timer variables
time_passed = 0
cam_initialized = False
cam_uptime = 10 #in seconds

#Frame variables
n_frames_segundos = 5
n_frames_totales = cam_uptime * n_frames_segundos  #Era 3
#frames_per_second = 20 
frame_counter = 0

while True:
    time_start = time.time()
    #print(time_passed)
    
    time_end = time.time()
    time_passed += time_end - time_start
    frame_counter+=1
'''

############################################################## ROUTES

cam_available = 0

@app.route('/', methods=['GET'])
def index():
    if(getCam() == 0):
        print("No hay camara conectada!")
    # rendering webpage
    return render_template('landing.html')
@app.route('/main', methods=['GET'])
def main():
    # rendering webpage
    return render_template('main.html', cam_available = cam_available)
def gen(camera):
    while True:        
        #get camera frame
        frame, got_landmarks = camera.get_frame()
        global cam_available
        cam_available = got_landmarks
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/static/images/video_feed')
def video_feed():   
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/check_cam', methods = ['GET'])
def check_cam():
    response = {"available":cam_available}
    return jsonify(response)

@app.route('/has_cam', methods = ['GET'])
def has_cam():
    if(getCam()):
         response = {"available":1}
    else:
         response = {"available":0}
    return jsonify(response)

if __name__ == '__main__':
    # defining server ip address and port    
    app.run(port='5000', debug=True)