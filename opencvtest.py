from picamera2 import Picamera2
import cv2



picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(config)
picam2.start()


try:
    while True:
        frame = picam2.capture_array()

        # Optional: convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Show frame in a window
        cv2.imshow("Camera Feed", gray)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
