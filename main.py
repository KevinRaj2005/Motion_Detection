import threading
import winsound
import cv2
import imutils
import numpy as np
import face_recognition

# Load your uploaded image and encode the face
known_image = face_recognition.load_image_file("C:\Motion_Detection\ronaldo.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# Add the known face and name
known_face_encodings = [known_face_encoding]
known_face_names = ["Ronaldo"]  # Replace with the name you want

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0
alarm_thread = None  # Keep track of the thread

def beep_alarm():
    global alarm
    while alarm:  # Keep beeping while the alarm is on
        print("ALARM BEEPING")  # Check if the beep starts
        winsound.Beep(2500, 1000)

while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(start_frame, frame_bw)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]

        # Check if motion is detected
        print(f"Threshold sum: {threshold.sum()}")  # Print threshold sum for debugging
        if threshold.sum() > 5000:  # Reduce the motion sensitivity threshold
            alarm_counter += 1
            print(f"Motion detected! Counter: {alarm_counter}")  # Debug motion detection

            # Perform face detection when motion is detected
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB for face_recognition
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            known_face_detected = False  # Reset the flag for each frame

            if face_encodings:
                print("Face detected!")  # Debugging face detection
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        print(f"Face recognized: {name}")  # Check if your face is recognized
                        known_face_detected = True  # Set the flag to True if a known face is recognized
                    else:
                        print("Face not recognized.")  # Debug non-matching face

                    # Draw a rectangle around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Only trigger the alarm if no known face is detected
            if not known_face_detected:
                if alarm_counter > 5:  # Adjusted for alarm triggering
                    if not alarm:
                        alarm = True
                        alarm_thread = threading.Thread(target=beep_alarm)
                        alarm_thread.start()  # Start the alarm thread
            else:
                # Reset the alarm counter if a known face is detected
                alarm_counter = 0

        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)
    elif not alarm_mode and alarm:
        black_frame = np.zeros_like(frame)
        cv2.imshow("Cam", black_frame)
    else:
        cv2.imshow("Cam", frame)

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord('t'):
        print("You have activated/deactivated the alarm!")
        alarm_mode = not alarm_mode
        alarm_counter = 0
        if not alarm_mode:
            alarm = False  # Stop the alarm when alarm_mode is deactivated
            if alarm_thread and alarm_thread.is_alive():
                alarm_thread.join()  # Ensure the alarm thread stops
        else:
            _, start_frame = cap.read()
            start_frame = imutils.resize(start_frame, width=500)
            start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
            start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

    elif key_pressed == ord('q'):
        print("Quitting the program!")
        alarm_mode = False
        alarm = False  # Ensure alarm stops before quitting
        if alarm_thread and alarm_thread.is_alive():
            alarm_thread.join()  # Ensure the alarm thread stops
        break

cap.release()
cv2.destroyAllWindows()
