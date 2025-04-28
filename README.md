
# Motion Detection and Face Recognition Alarm System

Description

This project implements a real-time Motion Detection and Face Recognition Alarm System using Python. It captures webcam video, detects motion, and checks if any known faces are present. If unknown movement is detected and the face is not recognized after a few frames, a loud beeping alarm is triggered as a security alert. The system is lightweight and ideal for personal security, home monitoring, and basic surveillance setups.

## Features

🛡️ Real-time motion detection based on frame differencing.

🎯 Face recognition using pre-uploaded images (e.g., "Ronaldo").

🔔 Alarm system that activates if no known face is detected.

🎥 Live webcam feed with face bounding boxes and labels.

🧠 Threaded alarm sound for smooth operation.

🖱️ Easy controls:

Press 't' to toggle the alarm ON/OFF.

Press 'q' to quit the application safely.


## Installation

1. Clone the repository

```bash
  git clone https://github.com/KevinRaj2005/Motion_Detection.git
  cd Motion_Detection
```
2. Install dependencies Make sure you have Python 3 installed. Then install the required libraries:

```bash
  pip install opencv-python
  pip install imutils
  pip install face_recognition
```
3. Prepare known faces

        Add an image (for example, ronaldo.jpg) in the project folder.

        Update the image path in the code if necessary.

4. Run the project
```bash 
  python motion_face_alarm.py                
```
## Future Improvements

Add Email/SMS alerts when intrusion is detected.

Record short video clips during alarms.

Add GUI controls for starting/stopping the system.

Support multiple known faces.

Improve face recognition accuracy in low light.