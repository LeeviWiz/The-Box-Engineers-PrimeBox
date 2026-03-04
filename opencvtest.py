import cv2
import numpy as np
from picamera2 import Picamera2
from flask import Flask, Response

app = Flask(__name__)

# =========================
# Load logo with alpha support
# =========================
logo_rgba = cv2.imread("logo.jpg", cv2.IMREAD_UNCHANGED)  # Use PNG with transparency
if logo_rgba is None:
    print("Logo not found!")
    exit()

# Separate channels
if logo_rgba.shape[2] == 4:
    b, g, r, a = cv2.split(logo_rgba)
    logo_gray = cv2.cvtColor(cv2.merge([b, g, r]), cv2.COLOR_BGR2GRAY)
    mask = a > 0  # Only detect features on non-transparent pixels
else:
    # No alpha, create mask for non-white pixels
    logo_gray = cv2.cvtColor(logo_rgba, cv2.COLOR_BGR2GRAY)
    mask = logo_gray < 250  # ignore almost-white background

# =========================
# ORB setup
# =========================
orb = cv2.ORB_create(nfeatures=1000, scaleFactor=1.1, edgeThreshold=35, patchSize=35)
kp1, des1 = orb.detectAndCompute(logo_gray, mask.astype(np.uint8))  # Apply mask here

bf = cv2.BFMatcher()

# =========================
# Camera setup
# =========================
picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    )
)
picam2.start()


def generate_frames():
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        kp2, des2 = orb.detectAndCompute(gray, None)

        detected = False

        if des1 is not None and des2 is not None and len(des2) > 1:
            matches = bf.knnMatch(des1, des2, k=2)

            good = []
            for match in matches:
                # Safe KNN unpacking
                if len(match) == 2:
                    m, n = match
                    if m.distance < 0.85 * n.distance:
                        good.append(m)

            # Require enough good matches
            if len(good) > 20:
                # Homography for extra accuracy
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

                M, mask_h = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                if M is not None:
                    detected = True

                    # Draw bounding box
                    h, w = logo_gray.shape
                    pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
                    dst = cv2.perspectiveTransform(pts, M)
                    frame = cv2.polylines(frame, [np.int32(dst)], True, (0, 255, 0), 3)

        # Overlay detection status
        status_text = "DETECTED" if detected else "NOT DETECTED"
        color = (0, 255, 0) if detected else (0, 0, 255)
        cv2.putText(frame, status_text, (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        print(detected)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)