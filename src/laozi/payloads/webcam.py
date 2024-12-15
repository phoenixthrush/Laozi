import tempfile
import os

import cv2


def get_webcam_snapshot():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return

    ret, frame = cap.read()

    if ret:
        temp_dir = tempfile.gettempdir()
        output_filename = os.path.join(temp_dir, "webcam_snapshot.jpg")

        cv2.imwrite(output_filename, frame)
        print(f"Snapshot saved at {output_filename}")
    else:
        print("Error: Failed to capture image.")

    cap.release()
    cv2.destroyAllWindows()

    return output_filename
