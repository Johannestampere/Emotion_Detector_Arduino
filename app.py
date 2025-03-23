import cv2 as cv
import numpy as np
import serial
from tensorflow.python.keras.models import load_model

model = load_model('./face_model.h5')

emotions = {
    0: "Angry",
    1: "Disgust",
    2: "Fear",
    3: "Happy",
    4: "Sad",
    5: "Surprise",
    6: "Neutral"
}

emotion_to_char = {
    "Angry": 'a',
    "Disgust": 'd',
    "Fear": 'f',
    "Happy": 'h',
    "Sad": 's',
    "Surprise": 'p',
    "Neutral": 'n'
}

cam = cv.VideoCapture(0)

frame_width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))
fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter('./videos/output.mp4', fourcc, 20.0, (frame_width, frame_height))

arduino = serial.Serial('/dev/cu.usbmodem14101', 9600) # mac usb port and arduino port nr

def preprocess(frame):
    resized_frame = cv.resize(frame, (48, 48))

    gray_frame = cv.cvtColor(resized_frame, cv.COLOR_BGR2GRAY)

    normalized_frame = gray_frame / 255.0

    input_frame = np.expand_dims(normalized_frame, axis=0) 
    input_frame = np.expand_dims(input_frame, axis=-1) 


    return input_frame

def send_emotion(emotion):
    arduino.write(emotion_to_char[emotion].encode())

while True:
    ret, frame = cam.read()
    if not ret:
        break

    input_frame = preprocess(frame)

    predictions = model.predict(input_frame)
    emotion_index = np.argmax(predictions)
    emotion = emotions[emotion_index]

    send_emotion(emotion)

    cv.putText(frame, f"Emotion: {emotion}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv.imshow('Camera', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
out.release()
cv.destroyAllWindows()
arduino.close()