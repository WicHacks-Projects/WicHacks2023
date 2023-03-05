import cv2
import numpy as np
import mediapipe as mp
import tkinter.colorchooser as colorchooser

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Initialize the hand tracking module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Get the frame size
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize the drawing canvas, color, and the previous point
canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
canvas[..., 0] = 0  # Set the canvas to black
canvas[..., 1] = 0  # Set the canvas to black
canvas[..., 2] = 0  # Set the canvas to black
color = (0, 0, 255)  # Set the default color to red
prev_x, prev_y = 0, 0

drawing = True
color_picker_open = False
while True:
    # Capture a frame from the video feed
    ret, frame = cap.read()
    
    # Flip the frame horizontally (mirror effect)
    frame = cv2.flip(frame, 1)
     # Resize the canvas to match the size of the frame
    canvas_resized = cv2.resize(canvas, (frame_width, frame_height))

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect the hand landmarks in the frame
    results = hands.process(frame_rgb)
    
    # Draw the landmarks and connect them with lines
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

            if thumb_tip.x < pinky_mcp.x:
                hand = "right"
            else:
                hand = "left"

            # Draw the landmarks and connect them with lines
            finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            cx, cy = int(finger_tip.x * frame_width), int(finger_tip.y * frame_height)
            
            # Connect the finger tip with the previous point
            if prev_x != 0 and prev_y != 0:
                cv2.line(canvas, (prev_x, prev_y), (cx, cy), (color[2], color[1], color[0]), thickness=5)

            # Update previous point to current point
            prev_x, prev_y = cx, cy
            if (thumb_tip.x < index_finger_tip.x and
                thumb_tip.x < middle_finger_tip.x and
                thumb_tip.x < ring_finger_tip.x and
                thumb_tip.x < pinky_tip.x and
                thumb_tip.y > index_finger_tip.y and
                thumb_tip.y > middle_finger_tip.y and
                thumb_tip.y > ring_finger_tip.y and
                thumb_tip.y > pinky_tip.y):
                
                color = colorchooser.askcolor()[0]
                color = tuple([int(c) for c in color]) # convert the color values to integers and create a tuple
            else:
                color_picker_open = False
                color_picker_open = False

    # Show the canvas in a separate window
    cv2.imshow('Canvas', canvas)
    
    # Combine the frame and the canvas
    frame_with_canvas = cv2.add(frame, canvas_resized)
    
    # Show the webcam feed in a separate window
    cv2.imshow('Webcam', frame_with_canvas)
    
    # Quit the program if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

    # Clear the canvas and video feed when 'c' is pressed
    if cv2.waitKey(1) == ord('c'):
        canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        canvas[..., 0] = 255  # Set the canvas to blue
        canvas[..., 1] = 255  # Set the canvas to green
        canvas[..., 2] = 0  # Set the canvas to yellow (swap red and blue channels)
        canvas.fill(0)  # Set the canvas to white
        color = (0, 0, 255)  # Set the default color to red
        prev_x, prev_y = 0, 0
# Release the resources
cap.release()
cv2.destroyAllWindows() 