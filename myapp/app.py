import random
from flask import Flask, Response, redirect, render_template, request, session
from twilio.rest import Client
# import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import cv2
import numpy as np
import mediapipe as mp

app = Flask(__name__)


# Define parameters for the camera
camera_index = 0  # Index of the camera to use
camera_width = 640
camera_height = 480

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

# Define parameters for the canvas
canvas_width = 640
canvas_height = 480
#canvas_thickness = 3

# Create a blank canvas
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

# Define route for the video feed
def gen():
    while True:
        ret, frame = cap.read()
        # your existing code for processing the frame and updating the canvas
        # yield the canvas as a JPEG image
        frame = cv2.imencode('.jpg', canvas)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
# Define route for the main page
@app.route('/')
def index():
    return render_template('home.html')

# Define route for the video stream
@app.route('/draw')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.secret_key = 'mysecretkey'
    app.run(debug=True)