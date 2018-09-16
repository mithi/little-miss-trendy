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



# Status either in left lane of right lane
STATUS = None
LEFT = 1
RIGHT = 2

FORKGORIGHT = 3
FORKGOLEFT = 4

# Global MODEL variables instatiated
# Load from file upon starting the script in __main__
MODEL = None
MODEL_LEFT = None
MODEL_RIGHT = None
MODEL_OBSTACLE = None

# Tweak parameters to adjust the throttle
MAX_SPEED = 2.0
MAX_ANGLE = 45.0
THROTTLE_MAX = 0.60 # 0.7
THROTTLE_MIN = 0.005
C_SPEED = 0.9 # 1.0
C_STEER = 30.0 # 20

# Crop and reshape parameters for lane driving
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


def switch_right():
    MODEL = MODEL_GREEN
    STATUS = LEFT
    send_control(45, 1.0)


def switch_left():
    MODEL = MODEL_RED
    STATUS = RIGHT
    send_control(-45, 1.0)


def predict_steer(img):
    image_array = process_image(np.asarray(image))
    steering_angle = float(MODEL.predict(image_array[None, :, :, :]))
    return steering_angle


def obstacle_detected(image):
    # process image
    # predict
    return False


@sio.on('telemetry')
def telemetry(sid, data):

    if data:

        # Get data from simlator
        steering_angle = float(data["steering_angle"])
        throttle = float(data["throttle"])
        speed = float(data["speed"])
        img_string = data["image"]

        image = Image.open(BytesIO(base64.b64decode(img_string)))

        if obstact_detected():
            if STATUS == LEFT:
                switch_right()
            if STATUS == RIGHT:
                switch_left()
            return

        sign = predict_sign(image)
        if  STATUS == LEFT and sign == FORKGORIGHT:
            switch_right()
            return
        if STATUS == RIGHT and sign == FORKGOLEFT:
            switch_left()
            return

        steering_angle = predict_steer(image)
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
        'leftmodel',
        type=str,
        help='Path to left model h5 file. Model should be on the same path.'
    )

    parser.add_argument(
        'rightmodel',
        type=str,
        help='Path to right model h5 file. Model should be on the same path.'
    )

    parser.add_argument(
        'obstaclemodel',
        type=str,
        help='Path to right model h5 file. Model should be on the same path.'
    )

    args = parser.parse_args()
    MODEL_LEFT = load_model(args.leftmodel)
    MODEL_RIGHT = load_model(args.rightmodel)
    MODEL_OBSTACLE = load_model(args.obstaclemodel)

    MODEL = MODEL_LEFT
    STATUS = LEFT

    app = socketio.Middleware(sio, Flask(__name__))
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 4567)), app)
