import cv2
import numpy as np

for i in range(10):
    print("Thinking inside the box! If anyone needs me, I'll be in my box - thinking...")

capture = cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()
    if not ret:
        break
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break