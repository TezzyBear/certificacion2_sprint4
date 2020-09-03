import cv2
import numpy as np
import dlib
import pandas as pd #pandas 1.0.3
import time
import datetime #pip install dateTime 4.3

#from webApp import app  --- PARA SERVER

#sp = "var/www/webApp/webApp/shape_predictor_68_face_landmarks.dat" --- PARA SERVER

sp = "shape_predictor_68_face_landmarks.dat"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(sp)

cameraOn = False
numpyArray = np.array([])

class VideoCamera:

    def __init__(self):
        #capturing video
        self.cap = getCam()
        #stackoverflowsaso con cap cuando es nulo
        self.prediction_points = []
        #array for data frame
        
    def __del__(self):
        #releasing camera
        self.cap.release()

    def get_frame(self):
        global numpyArray    
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

            fila = []

            for i in range(0, 68):       
                cv2.circle(frame, (landmarks.part(i).x,landmarks.part(i).y), 4, (255, 0, 0), -1)
                face_points.append((landmarks.part(i).x,landmarks.part(i).y))
                xToAppend = landmarks.part(i).x
                yToAppend = landmarks.part(i).y

                fila.append(xToAppend)
                fila.append(yToAppend)
            
            global cameraOn
            if cameraOn:
                if len(numpyArray) == 0:
                    numpyArray = np.array([fila])
                else:
                    numpyArray = np.vstack((numpyArray, fila))

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

def start_Recoding():
    global numpyArray 
    numpyArray = np.array([])
    global cameraOn
    cameraOn = True

def stop_Recording():
    global cameraOn
    cameraOn = False
    global numpyArray   

def get_numpyArray():
    global numpyArray
    return numpyArray    

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