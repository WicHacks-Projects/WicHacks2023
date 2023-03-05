import cv2
import numpy as np
import mediapipe as mp
from flask import Flask, Response, render_template

app = Flask(__name__)

# Initialize the hand tracking module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=10, min_detection_confidence=0.5)

# Get the frame size
camera_width = 640
camera_height = 480

# Initialize the video capture object
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

# Initialize the drawing canvas and the previous point
canvas = np.zeros((camera_height, camera_width, 3), dtype=np.uint8)
canvas.fill(255)  # Set the canvas to white

prev_x, prev_y = None, None

# Define route for the video stream
def gen():
    while True:
        # Capture a frame from the video feed
        ret, frame = cap.read()
        
        # Flip the frame horizontally (mirror effect)
        frame = cv2.flip(frame, 1)
        
        # Convert the frame to RGB for hand tracking
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect the hand landmarks in the frame
        results = hands.process(frame_rgb)
        
        # Draw the landmarks and connect them with lines
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Check if the hand is the left or right
                if hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x:
                    hand = "left"
                else:
                    hand = "right"
                    
                # Draw the landmarks and connect them with lines
                finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                cx, cy = int(finger_tip.x * camera_width), int(finger_tip.y * camera_height)
                
                # Connect the finger tip with the previous point
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (cx, cy), (0, 0, 255), thickness=5)

                # Update previous point to current point
                prev_x, prev_y = cx, cy
        
        # Show the canvas in a separate window
        cv2.imshow('Canvas', canvas)
        
        # Combine the frame and the canvas
        frame_with_canvas = cv2.add(frame, canvas)
        
        # Convert the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame_with_canvas)
        
        # Yield the frame as a JPEG image
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/draw')
def draw():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
