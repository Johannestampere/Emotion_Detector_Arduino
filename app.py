import cv2 as cv
import numpy as np
import serial
from tensorflow.keras.models import load_model

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

