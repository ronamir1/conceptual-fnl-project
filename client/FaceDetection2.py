import time

import cv2
from client.config import *
from datetime import datetime
import uuid
import requests


def detect(face_cascade):
    # Load the cascade2

    # To capture video from webcam.
    cap = cv2.VideoCapture(0)
    # To use a video file as input
    # cap = cv2.VideoCapture('filename.mp4')

    while True:
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            cap.release()
            return

        time.sleep(0.5)
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for i, (x, y, w, h) in enumerate(faces):
            # cv2.rectangle(img, (x - 0.5 * w, y - 0.5 * h), (x + 1.5 * w, y + 1.5 * h), (255, 0, 0), 2)
            roi = img[y - int(0.5 * h): y + int(1.5 * h), x - int(0.5 * w):x + int(1.5 * w)]
            if roi.size == 0:
                continue
            # Display
            uid = uuid.uuid4()
            path_local = f"person_{i}.jpg"
            image_name = f'{uid}${datetime.now().isoformat().replace(":", "-")}$.jpg'
            dest_path = f'{bus_id}/{cam_type}/{image_name}'
            cv2.imwrite(path_local, roi)
            # upload to server
            storage.child(dest_path).put(path_local)
            data = {'image_url': image_name}
            r = requests.post(f'{BASE_API}/upload/{bus_id}/{cam_type}/{index}', data=data)
            if not r.ok:
                if cam_type == "entranceCam":
                    storage.delete(dest_path)
                continue

            response = r.json()
            print(response)
        # cv2.imshow('img', img)


# Release the VideoCapture object


def main():
    face_cascade = cv2.CascadeClassifier(xml_path)
    detect(face_cascade)


if __name__ == '__main__':
    main()
