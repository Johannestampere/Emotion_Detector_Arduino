import cv2 as cv
import numpy as np
import serial
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore

model = load_model('face_model.h5')

class_names = ['Angry', 'Disgusted', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

emotion_to_char = {
    "Angry": 'a',
    "Fear": 'f',
    "Happy": 'h',
    "Sad": 's',
    "Neutral": 'n'
}

def send_emotion(emotion):
    if arduino is not None and emotion in emotion_to_char:
        arduino.write(emotion_to_char[emotion].encode())

cam = cv.VideoCapture(0)

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cam.read()
    arduino = serial.Serial('/dev/cu.usbmodem14401', 9600)  # Update with your port

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_roi = frame[y:y + h, x:x + w]
        face_image = cv.resize(face_roi, (48, 48))
        face_image = cv.cvtColor(face_image, cv.COLOR_BGR2GRAY)
        face_image = image.img_to_array(face_image)
        face_image = np.expand_dims(face_image, axis=0)
        face_image = np.vstack([face_image])

        predictions = model.predict(face_image)
        emotion_label = class_names[np.argmax(predictions)]

        send_emotion(emotion_label)

        cv.putText(frame, f'Emotion: {emotion_label}', (x, y - 10), cv.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 0, 255), 2)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.imshow('Emotion Detection', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

# happy - sinine
# fear - oranz
# angry - punane
# neutral - valge