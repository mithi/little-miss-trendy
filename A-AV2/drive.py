import argparse
import base64
from datetime import datetime
import os
import shutil

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO
from keras.models import load_model

import cv2
import pandas as pd
import numpy as np
import matplotlib.image as mpimg

MODEL = None
MAX_SPEED = 2.0
MAX_ANGLE = 45.0
THROTTLE_MAX = 0.70 # 0.72, 0.6
C_SPEED = 1.0 # 0.9, 1.1, 1.5
C_STEER = 20.0 # 10, 15.0

INPUT_H, INPUT_W = 75, 200
INPUT_SHAPE = (INPUT_H, INPUT_W, 3)
# Crop parameters
YSTART = 110
YSTOP = 230


sio = socketio.Server()


def process_image(img):
    img = img[YSTART:YSTOP, :, :]
    img = cv2.resize(img, (INPUT_W, INPUT_H), cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    return img


def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data = {
            'steering_angle': str(steering_angle),
            'throttle': str(throttle)
        },
        skip_sid=True)


@sio.on('telemetry')
def telemetry(sid, data):

    if data:

        steering_angle = float(data["steering_angle"])
        throttle = float(data["throttle"])
        speed = float(data["speed"])
        img_string = data["image"]

        image = Image.open(BytesIO(base64.b64decode(img_string)))
        image_array = process_image(np.asarray(image))
        steering_angle = float(MODEL.predict(image_array[None, :, :, :]))

        throttle = THROTTLE_MAX - C_SPEED * (speed / MAX_SPEED)**2 - C_STEER * (steering_angle / MAX_ANGLE)**2
        throttle = max(0.002, throttle)

        #print()
        #print("PREVIOUS angle:", steering_angle, " | speed:", speed, " | throttle:", throttle)
        #print("CONTROL angle:", steering_angle, "throttle:", throttle);
        #print()

        send_control(steering_angle, throttle)

    else:
        sio.emit('manual', data={}, skip_sid=True)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0.0, 0.0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto Driving!')
    parser.add_argument(
        'model',
        type=str,
        help='Path to model h5 file. Model should be on the same path.'
    )

    args = parser.parse_args()
    MODEL = load_model(args.model)

    app = socketio.Middleware(sio, Flask(__name__))
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 4567)), app)
