import cv2
import numpy as np
import dlib
import math
from math import hypot
import sys
from time import time
import random

camera = cv2.VideoCapture(0)
path = ""


def main_frames(name):
    if name == 'dog':
        nose_image = cv2.imread("./static/animals/dog_nose.png")
        ears_image = cv2.imread("./static/animals/dog_ears.png")
        _, frame1 = camera.read()
        rows, cols, _ = frame1.shape
        ears_mask = np.zeros((rows, cols), np.uint8)
        nose_mask = np.zeros((rows, cols), np.uint8)
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(
            "./prebild_models/shape_predictor_68_face_landmarks.dat")
        while True:
            _, frame1 = camera.read()
            try:
                ears_mask.fill(0)
                nose_mask.fill(0)
                gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
                faces = detector(gray_frame1)
                for face in faces:
                    landmarks = predictor(gray_frame1, face)
                    left_forehead = (landmarks.part(
                        19).x, landmarks.part(19).y)
                    right_forehead = (landmarks.part(26).x,
                                      landmarks.part(26).y)
                    center_forehead = (landmarks.part(28).x,
                                       landmarks.part(28).y)
                    forehead_width = int(hypot(
                        left_forehead[0]-right_forehead[0], left_forehead[1]-right_forehead[1])*2.6)
                    forehead_height = int(forehead_width*0.77)
                    top_left_ears = (
                        int(center_forehead[0]-forehead_width/2), int(center_forehead[1]-forehead_height))
                    bottom_right_ears = (
                        int(center_forehead[0]+forehead_width/2), int(center_forehead[1]+forehead_height))
                    dog_ears = cv2.resize(
                        ears_image, (forehead_width, forehead_height))
                    dog_ears_gray = cv2.cvtColor(dog_ears, cv2.COLOR_BGR2GRAY)
                    _, ears_mask = cv2.threshold(
                        dog_ears_gray, 25, 255, cv2.THRESH_BINARY_INV)
                    ears_area = frame1[top_left_ears[1]:top_left_ears[1]+forehead_height,
                                       top_left_ears[0]:top_left_ears[0]+forehead_width]
                    top_nose = (landmarks.part(29).x, landmarks.part(29).y)
                    center_nose = (landmarks.part(30).x, landmarks.part(30).y)
                    left_nose = (landmarks.part(31).x, landmarks.part(31).y)
                    right_nose = (landmarks.part(35).x, landmarks.part(35).y)
                    nose_width = int(hypot(left_nose[0] - right_nose[0],
                                           left_nose[1] - right_nose[1]) * 1.7)
                    nose_height = int(nose_width * 0.77)
                    top_left_nose = (int(center_nose[0] - nose_width / 2),
                                     int(center_nose[1] - nose_height / 2))
                    bottom_right_nose = (int(center_nose[0] + nose_width / 2),
                                         int(center_nose[1] + nose_height / 2))
                    nose_pig = cv2.resize(
                        nose_image, (nose_width, nose_height))
                    nose_pig_gray = cv2.cvtColor(nose_pig, cv2.COLOR_BGR2GRAY)
                    _, nose_mask = cv2.threshold(
                        nose_pig_gray, 25, 255, cv2.THRESH_BINARY_INV)
                    nose_area = frame1[top_left_nose[1]: top_left_nose[1] + nose_height,
                                       top_left_nose[0]: top_left_nose[0] + nose_width]
                    ears_area_no_ears = cv2.bitwise_and(
                        ears_area, ears_area, mask=ears_mask)
                    nose_area_no_nose = cv2.bitwise_and(
                        nose_area, nose_area, mask=nose_mask)
                    frame1 = frame1
                    final_ears = cv2.add(ears_area_no_ears, dog_ears)
                    frame1[top_left_ears[1]: top_left_ears[1]+forehead_height,
                           top_left_ears[0]:top_left_ears[0]+forehead_width] = final_ears
                    final_nose = cv2.add(nose_area_no_nose, nose_pig)
                    frame1[top_left_nose[1]: top_left_nose[1] + nose_height,
                           top_left_nose[0]: top_left_nose[0] + nose_width] = final_nose
            except:
                _, frame2 = camera.read()
                ret, buffer = cv2.imencode('.jpg', frame2)
                frame2 = buffer.tobytes()
                yield (b'--frame2\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')
            else:
                ret, buffer = cv2.imencode('.jpg', frame1)
                frame1 = buffer.tobytes()
                yield (b'--frame1\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')
    if name == 'pig':
        nose_image = cv2.imread("./static/animals/pig_nose.png")
        _, frame3 = camera.read()
        rows, cols, _ = frame3.shape
        nose_mask = np.zeros((rows, cols), np.uint8)
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(
            "./prebild_models/shape_predictor_68_face_landmarks.dat")
        while True:
            success, frame3 = camera.read()
            try:
                nose_mask.fill(0)
                gray_frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
                faces = detector(gray_frame3)
                for face in faces:
                    landmarks = predictor(gray_frame3, face)
                    top_nose = (landmarks.part(29).x, landmarks.part(29).y)
                    center_nose = (landmarks.part(30).x, landmarks.part(30).y)
                    left_nose = (landmarks.part(31).x, landmarks.part(31).y)
                    right_nose = (landmarks.part(35).x, landmarks.part(35).y)
                    nose_width = int(hypot(left_nose[0] - right_nose[0],
                                           left_nose[1] - right_nose[1]) * 1.7)
                    nose_height = int(nose_width * 0.77)
                    top_left = (int(center_nose[0] - nose_width / 2),
                                int(center_nose[1] - nose_height / 2))
                    bottom_right = (int(center_nose[0] + nose_width / 2),
                                    int(center_nose[1] + nose_height / 2))
                    nose_pig = cv2.resize(
                        nose_image, (nose_width, nose_height))
                    nose_pig_gray = cv2.cvtColor(nose_pig, cv2.COLOR_BGR2GRAY)
                    _, nose_mask = cv2.threshold(
                        nose_pig_gray, 25, 255, cv2.THRESH_BINARY_INV)
                    nose_area = frame3[top_left[1]: int(top_left[1] + nose_height),
                                       top_left[0]: int(top_left[0] + nose_width)]
                    nose_area_no_nose = cv2.bitwise_and(
                        nose_area, nose_area, mask=nose_mask)
                    final_nose = cv2.add(nose_area_no_nose, nose_pig)
                    frame3[top_left[1]: top_left[1] + nose_height,
                           top_left[0]: top_left[0] + nose_width] = final_nose
            except:
                _, frame4 = camera.read()
                ret, buffer = cv2.imencode('.jpg', frame4)
                frame4 = buffer.tobytes()
                yield (b'--frame4\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame4 + b'\r\n')
            else:
                ret, buffer = cv2.imencode('.jpg', frame3)
                frame3 = buffer.tobytes()
                yield (b'--frame3\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame3 + b'\r\n')
    if name == 'panda':
        panda_image = cv2.imread("./static/animals/panda_face.png")
        _, frame5 = camera.read()
        rows, cols, _ = frame5.shape
        panda_mask = np.zeros((rows, cols), np.uint8)
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(
            "./prebild_models/shape_predictor_68_face_landmarks.dat")
        while True:
            _, frame5 = camera.read()
            try:
                panda_mask.fill(0)
                gray_frame5 = cv2.cvtColor(frame5, cv2.COLOR_BGR2GRAY)

                faces = detector(gray_frame5)
                for face in faces:
                    # logic behind the filter
                    landmarks = predictor(gray_frame5, face)
                    left_pandaface = (landmarks.part(1).x, landmarks.part(1).y)
                    right_pandaface = (landmarks.part(17).x,
                                       landmarks.part(17).y)
                    center_pandaface = (landmarks.part(
                        28).x, landmarks.part(28).y)
                    pandaface_width = int(hypot(
                        left_pandaface[0]-right_pandaface[0], left_pandaface[1]-right_pandaface[1])*7.0)
                    pandaface_height = int(pandaface_width*0.81)
                    top_left = (int(
                        center_pandaface[0]-pandaface_width/2), int(center_pandaface[1]-pandaface_height/2))
                    bottom_right = (int(
                        center_pandaface[0]+pandaface_width/2), int(center_pandaface[1]+pandaface_height/2))
                    panda_face = cv2.resize(
                        panda_image, (pandaface_width, pandaface_height))
                    panda_face_gray = cv2.cvtColor(
                        panda_face, cv2.COLOR_BGR2GRAY)
                    _, pandaface_mask = cv2.threshold(
                        panda_face_gray, 25, 255, cv2.THRESH_BINARY_INV)
                    pandaface_area = frame5[top_left[1]:top_left[1]+pandaface_height,
                                            top_left[0]:top_left[0]+pandaface_width]
                    pandaface_area_no_face = cv2.bitwise_and(
                        pandaface_area, pandaface_area, mask=pandaface_mask)
                    frame5 = frame5
                    final_pandaface = cv2.add(
                        pandaface_area_no_face, panda_face)
                    frame5[top_left[1]: top_left[1]+pandaface_height,
                           top_left[0]:top_left[0]+pandaface_width] = final_pandaface
            except:
                _, frame6 = camera.read()
                ret, buffer = cv2.imencode('.jpg', frame6)
                frame6 = buffer.tobytes()
                yield (b'--frame6\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame6 + b'\r\n')
            else:
                ret, buffer = cv2.imencode('.jpg', frame5)
                frame5 = buffer.tobytes()
                yield (b'--frame5\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame5 + b'\r\n')
  