from flask import Flask, render_template, redirect, url_for, Response, jsonify
from camera import VideoCamera, getCam, start_Recoding, stop_Recording, get_numpyArray
from prediction import get_prediction, getMeassurements, Meassurements
import numpy as np
import json
app = Flask(__name__)

#import webApp.camera  --- PARA SERVER

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

@app.route('/stopRecording', methods=['GET'])
def stopRecording():
    print("Stopped")
    ## get_prediction(get_numpyArray(), 10)
    stop_Recording()
    return json.dumps(getMeassurements().__dict__)

@app.route('/startRecording', methods=['GET'])
def startRecording():
    print("Started")
    start_Recoding()
    return ("nothing")


@app.route('/details', methods = ['GET'])
def details():
    return render_template('details.html', meassurements = getMeassurements())

if __name__ == '__main__':
    # defining server ip address and port    
    app.run(port='5001', debug=True)

