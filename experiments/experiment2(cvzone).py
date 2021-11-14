from cvzone.HandTrackingModule import HandDetector
import cv2 as cv

capture = cv.VideoCapture("/dev/video0")
detector = HandDetector(detectionCon=0.5, maxHands=1)

while True:
    isTrue, frame = capture.read()
    frame = detector.findHands(frame)
    lmList, bbox = detector.findPosition(frame)
    
    cv.imshow("Vid", frame)
    
    if cv.waitKey(20) & 0xFF==ord("q"):
        break
    
capture.release()
cv.destroyAllWindows()
    
    