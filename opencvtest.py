from picamera2 import Picamera2
import cv2
import numpy as np
from flask import Flask, Response

app = Flask(__name__)

# ---------------------------
# REFERENTIE
# ---------------------------
reference_image = cv2.imread("logo.jpg")

if reference_image is None:
    print("FOUT: Afbeelding niet gevonden!")
    exit()

reference_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create(nfeatures=1500)

kp1, des1 = orb.detectAndCompute(reference_gray, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# ---------------------------
# CAMERA
# ---------------------------
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

print("Server Started")

# ---------------------------
# FRAME GENERATOR
# ---------------------------
def generate_frames():

    while True:

        detected = False

        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        kp2, des2 = orb.detectAndCompute(gray, None)

        if des2 is not None:

            matches = bf.knnMatch(des1, des2, k=2)

            good_matches = []

            for m, n in matches:
                if m.distance < 0.80 * n.distance:
                    good_matches.append(m)

            if len(good_matches) > 25:

                src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)

                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                if M is not None and mask is not None and mask.sum() > 25:

                    detected = True

                    h, w = reference_gray.shape
                    pts = np.float32([[0,0],[0,h],[w,h],[w,0]]).reshape(-1,1,2)
                    dst = cv2.perspectiveTransform(pts, M)

                    frame = cv2.polylines(frame, [np.int32(dst)], True, (0,255,0), 3)
                    cv2.putText(frame, "Logo Recognized", (50,50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # 🔹 Print detection status
        print(detected)

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# ---------------------------
# WEB ROUTE
# ---------------------------
@app.route('/')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# ---------------------------
# START SERVER
# ---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)