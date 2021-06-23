from flask import Flask, request
import os
import pyrebase
import face_recognition
from pathlib import Path

app = Flask(__name__)

config = {"apiKey": "AIzaSyCM1MwSxh3NGOJ5MuumUcRmlZKs_b5Sp0g",
          "authDomain": "inspectorapp-6d1d7.firebaseapp.com",
          "databaseURL": "https://inspectorapp-6d1d7.firebaseapp.com",
          "projectId": "inspectorapp-6d1d7",
          "storageBucket": "inspectorapp-6d1d7.appspot.com",
          "messagingSenderId": "1093381045628",
          "appId": "1:1093381045628:web:061bf8752b2bff363538f9",
          "serviceAccount": "inspectorapp-6d1d7-firebase-adminsdk-ao0uh-5ef626748a.json",
          "measurementId": "G-33MMBH01LN"}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
ENTRANCE = 'entranceCam'
PAID = 'paidCam'
UNKNOWN_IMAGE = 'Unknown image, added to suspect list'
PASSENGER_PAID = 'Passenger paid, removed from suspect list'
KNOWN_PASSENGER = 'Known Passenger, photo was not added'
BAD_IMAGE = 'Bad Image - cannot recognize face in image'


def _compare_face(known_images, image_to_check):
    result = face_recognition.compare_faces(known_images, image_to_check)
    return result


def get_request_args(form):
    return form.get('image_url'), form.get('bus_id'), form.get('cam_type')


def get_image_encodings(image_url):
    storage.child(image_url).download(image_url)
    new_image = face_recognition.load_image_file(image_url)
    return face_recognition.face_encodings(new_image)


def get_known_images_and_urls(path_on_cloud, image_name):
    known_images = []
    urls = []
    for f in storage.bucket.list_blobs(prefix=path_on_cloud):
        if f.name.endswith('.jpg') and f.name != path_on_cloud + "/" + image_name:
            Path(f.name).parent.mkdir(parents=True, exist_ok=True)
            old_encodings = get_image_encodings(f.name)
            if old_encodings:
                urls.append(f.name)
                known_images.extend(old_encodings)
    return known_images, urls


def generate_response(urls, results, cam_type, image_url):
    response = {'Result': UNKNOWN_IMAGE}, 200
    for url, res in zip(urls, results):
        if res:
            storage.delete(url)
            if cam_type == PAID:
                storage.delete(image_url)
                return {'Result': PASSENGER_PAID}, 200

            else:
                return {'Result': KNOWN_PASSENGER}, 200
    if cam_type == PAID:
        storage.delete(image_url)
    return response


@app.route('/upload', methods=['POST'])
def upload():
    image_name, bus_id, cam_type = get_request_args(request.form)

    image_url = f'{bus_id}/{cam_type}/{image_name}'
    path_on_cloud = f'{bus_id}/{ENTRANCE}'

    Path(image_url).parent.mkdir(parents=True, exist_ok=True)
    new_image_encodings = get_image_encodings(image_url)

    if not new_image_encodings:
        storage.delete(image_url)
        return {'Result': BAD_IMAGE}, 200

    known_images, urls = get_known_images_and_urls(path_on_cloud, image_name)

    results = _compare_face(known_images, new_image_encodings[0])
    return generate_response(urls, results, cam_type, image_url)


@app.route("/", methods=["GET"])
def hello():
    """ Return a friendly HTTP greeting. """
    who = request.args.get("who", "Hi")
    return f"Hello {who}!\n"


if __name__ == "__main__":
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host="localhost", port=8080, debug=True)
