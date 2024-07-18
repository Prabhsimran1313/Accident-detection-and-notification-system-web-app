import cv2
import numpy as np
import tempfile
import os
from detection import AccidentDetectionModel
from notification import AccidentNotification

model = AccidentDetectionModel("model.json", 'model_weights.h5')
notification = AccidentNotification()
font = cv2.FONT_HERSHEY_SIMPLEX


def process_input(file):
    notification = AccidentNotification()

    # Save the uploaded file temporarily
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)

    # Create a VideoCapture object from the file path
    video = cv2.VideoCapture(temp_path)

    frame_width = 640  # Adjust the desired width of the video frame
    frame_height = 480  # Adjust the desired height of the video frame

    # Create a resizable window
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

    # Set the window size
    cv2.resizeWindow('Video', frame_width, frame_height)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_frame, (224, 224))
        pred, prob = model.predict_accident(roi[np.newaxis, :, :])

        # Detect accident
        if prob > 0.855:  # Threshold adjusted to 0.7 (70%)
            notification.play_beep()
            if pred == "crash":
                # Get latitude and longitude (example values)
                accident_latitude = 28.6139
                accident_longitude = 77.2090
                notification.notify_accident(frame, accident_latitude, accident_longitude)
                return "Accident detected"

        result_text = f"{pred} {round(prob * 100, 2)}%"
        cv2.rectangle(frame, (0, 0), (300, 40), (0, 0, 0), -1)
        cv2.putText(frame, result_text, (10, 30), font, 1, (255, 255, 0), 2)

        cv2.imshow('Video', frame)
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    return "No accident detected"
