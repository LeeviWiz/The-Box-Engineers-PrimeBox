from picamera2 import Picamera2
import cv2
import numpy as np
import threading
from flask import Flask, Response

app = Flask(__name__)

class LogoDetector:

    def __init__(self):

        self.detected = False
        self.running = False
        self.frame = None

        reference_image = cv2.imread("/home/robox/The-Box-Engineers-PrimeBox/images/logo.jpg")

        if reference_image is None:
            raise Exception("Fault: could not find image")

        reference_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

        self.orb = cv2.ORB_create(nfeatures=1500)
        self.kp1, self.des1 = self.orb.detectAndCompute(reference_gray, None)

        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        self.reference_gray = reference_gray

        # camera will be created later
        self.picam2 = None

    def start_camera(self):

        if self.picam2 is None:
            self.picam2 = Picamera2()
            self.picam2.configure(
                self.picam2.create_preview_configuration(main={"size": (640,480)})
            )
            self.picam2.start()

            print("Camera Started")

    def _loop(self):

        while self.running:

            frame = self.picam2.capture_array()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            kp2, des2 = self.orb.detectAndCompute(gray, None)

            detected = False

            if des2 is not None:

                matches = self.bf.knnMatch(self.des1, des2, k=2)

                good = []
                for m,n in matches:
                    if m.distance < 0.8*n.distance:
                        good.append(m)

                if len(good) > 25:
                    detected = True

            self.detected = detected
            self.frame = frame

    def start(self):

        self.start_camera()

        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def generate_frames(self):

        while True:

            if self.frame is None:
                continue

            ret, buffer = cv2.imencode(".jpg", self.frame)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   buffer.tobytes() + b'\r\n')


detector = None


@app.route('/')
def video_feed():
    return Response(detector.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame')


def start_server():

    global detector

    detector = LogoDetector()
    detector.start()

    app.run(host="0.0.0.0", port=5000)