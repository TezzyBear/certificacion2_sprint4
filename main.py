from flask import Flask, render_template, Response, jsonify
from camera import VideoCamera

app = Flask(__name__)

cam_available = 0

@app.route('/', methods=['GET'])
def index():
    # rendering webpage
    return render_template('index.html', cam_available = cam_available)
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

@app.route('/test', methods = ['GET'])
def test():
    response = {"available":cam_available}
    return jsonify(response)

if __name__ == '__main__':
    # defining server ip address and port    
    app.run(port='5000', debug=True)

