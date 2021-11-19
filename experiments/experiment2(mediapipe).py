import cv2
import mediapipe as mp

capture = cv2.VideoCapture("/dev/video0")

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    isTrue, frame = capture.read()
    frame = cv2.flip(frame, 1) # Mirrors webcam input
    results = hands.process(frame)
    RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
    
    cv2.imshow("Video", frame)
    cv2.waitKey(1)
    