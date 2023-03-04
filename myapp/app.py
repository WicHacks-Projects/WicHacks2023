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

# Define parameters for the hand tracker and gesture recognition
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Define parameters for the canvas
canvas_width = 640
canvas_height = 480
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
# Define parameters for the hand movement generator
num_fingers = 5
num_joints_per_finger = 4
max_joint_angle = np.pi / 4  # Maximum angle for each joint in radians
# Define function to generate random hand movements
def generate_hand_movement():
    # Generate random joint angles for each finger
    joint_angles = np.random.uniform(-max_joint_angle, max_joint_angle, size=(num_fingers, num_joints_per_finger))

    # Flatten the joint angles into a 20-element array
    hand_movement = joint_angles.flatten()
    return hand_movement

# Define route for the main page
@app.route('/')
def index():
    return render_template('home.html')

# Define route for the video feed
def gen():
    while True:
        # Get the hand landmarks from the camera
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Get the landmarks and draw them on the canvas
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(canvas, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Generate a new hand movement and draw it on the canvas
        hand_movement = generate_hand_movement()
        # Code to use the hand movement to draw on the canvas goes here

        # Display the canvas
        ret, buffer = cv2.imencode('.jpg', canvas)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Define route for the video stream
@app.route('/video_feed')
def video_feed():
    return Response(video_feed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.secret_key = 'mysecretkey'
    app.run(debug=True)
    
    
