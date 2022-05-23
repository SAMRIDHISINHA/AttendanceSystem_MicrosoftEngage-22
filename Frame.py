from data import image_indir , image_name
from attendance import add_attendance
from data import image_indir,image_name
from faceEncoding import faceEncodings
import face_recognition
from importlib.resources import path
from tarfile import ENCODING
import cv2
from cv2 import findTransformECC
from base64 import encode
import numpy as np


images = image_indir()
personName = image_name()
encodListKnown = faceEncodings(images)
print("All encodings completed !!!!")

def get_frame(bool = True):
    if bool:
        cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)
        facesCurrentFrame = face_recognition.face_locations(faces)
        encodeCurrentFrame = face_recognition.face_encodings(
            faces, facesCurrentFrame)
        for encodeFace, faceLoc in zip(encodeCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(
                encodListKnown, encodeFace)
            facedis = face_recognition.face_distance(
                encodListKnown, encodeFace)
            matchIndex = np.argmin(facedis)
            if matches[matchIndex]:
                name = personName[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2-35), (x2, y2),
                              (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1+6, y2-6),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                try:
                    add_attendance(name)
                except:
                    pass
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()
