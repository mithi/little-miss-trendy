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

# Global MODEL variable instatiated to None
# load from file upon starting the script in __main__
MODEL = None

MAX_SPEED = 2.0
MAX_ANGLE = 45.0

# Tweak parameters to adjust the throttle
# throttle = THROTTLE_MAX - C_SPEED * (speed / MAX_SPEED)**2 - C_STEER * (steering_angle / MAX_ANGLE)**2
# throttle = max(THROTTLE_MIN, throttle)
THROTTLE_MAX = 0.79
THROTTLE_MIN = 0.01
C_SPEED = 1.0
C_STEER = 40.0


# BETA 3: RED - TRACK 1
# THROTTLE_MAX=0.6 C_STEER=50, THROTTLE_MIN=0.1, C_SPEED=1.0

# BETA 3: RED - TRACK 2, TRACK3
# THROTTLE_MAX=0.8, C_STEER=40, THROTTLE_MIN=0.1, C_SPEED=1.0

# Crop and reshape parameters
YSTART = 110
YSTOP = 230
INPUT_H, INPUT_W = 75, 200
INPUT_SHAPE = (INPUT_H, INPUT_W, 3)


# Initialize global Socket Server
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


def predict_steer(img_string):
    image = Image.open(BytesIO(base64.b64decode(img_string)))
    image_array = process_image(np.asarray(image))
    steering_angle = float(MODEL.predict(image_array[None, :, :, :]))
    return steering_angle

@sio.on('telemetry')
def telemetry(sid, data):

    if data:

        steering_angle = float(data["steering_angle"])
        throttle = float(data["throttle"])
        speed = float(data["speed"])
        img_string = data["image"]

        steering_angle = predict_steer(img_string)

        throttle = THROTTLE_MAX - C_SPEED * (speed / MAX_SPEED)**2 - C_STEER * (steering_angle / MAX_ANGLE)**2
        throttle = max(THROTTLE_MIN, throttle)

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
