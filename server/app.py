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


def _compare_face(known_images, image_to_check):
    result = face_recognition.compare_faces(known_images, image_to_check)
    print(result)
    return result


@app.route('/upload', methods=['POST'])
def upload():
    image_name = request.form.get('image_url')
    bus_id = request.form.get('bus_id')
    cam_type = request.form.get('cam_type')
    image_url = f'{bus_id}/{cam_type}/{image_name}'
    Path(image_url).parent.mkdir(parents=True, exist_ok=True)
    storage.child(image_url).download(image_url)
    new_image = face_recognition.load_image_file(image_url)
    new_image_encodings = face_recognition.face_encodings(new_image)

    if not new_image_encodings:
        storage.delete(image_url)
        return {'Result': 'Unrecognized image'}, 200
    path_on_cloud = f'{bus_id}/{ENTRANCE}'
    known_images = []
    urls = []
    for f in storage.bucket.list_blobs(prefix=path_on_cloud):
        if not f.name.endswith('.jpg') or f.name == image_name:
            continue
        Path(f.name).parent.mkdir(parents=True, exist_ok=True)
        storage.child(f.name).download(f.name)
        old_image = face_recognition.load_image_file(f.name)
        old_encodings = face_recognition.face_encodings(old_image)
        if not old_encodings:
            continue
        urls.append(f.name)
        known_images.extend(old_encodings)
        # res = _compare_face(new_image, old_image)
        # if res:
        #     if cam_type == PAID:
        #         storage.delete(f.name)
        #         paid = True
        #         continue
        #     storage.delete(image_url)
        #     return {"Result": 'Known image'}, 200
    result = _compare_face(known_images, new_image_encodings[0])
    response = {'Result': 'Unknown image'}, 200
    for url, res in zip(urls, result):
        if res:
            storage.delete(url)
            if cam_type == PAID:
                response = {'Result': 'User paid'}, 200

    if cam_type == PAID:
        storage.delete(image_url)
    return response


@app.route("/compare", methods=["POST"])
def compare_faces():
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    origin = request.form.get("origin")
    dest = request.form.get("dest")
    for f in storage.bucket.list_blobs(prefix=origin):
        if not f.name.endswith('.jpg'):
            continue
        fname = f.name.replace(':', '-')
        Path(fname).parent.mkdir(parents=True, exist_ok=True)
        storage.child(f.name).download(fname)
    for f in storage.bucket.list_blobs(prefix=dest):
        if not f.name.endswith('.jpg'):
            continue
        fname = f.name.replace(':', '-')
        Path(fname).parent.mkdir(parents=True, exist_ok=True)
        storage.child(f.name).download(fname)
    results = {}
    for f1 in os.listdir(origin):
        if f1.endswith(".jpg"):
            known_image = face_recognition.load_image_file(os.path.join(origin, f1))
            for f2 in os.listdir(dest):
                if f1.endswith(".jpg"):
                    unknown_image = face_recognition.load_image_file(os.path.join(dest, f2))
                    file_encodings = face_recognition.face_encodings(known_image)
                    file_encoding = file_encodings[0]
                    file2_encoding = face_recognition.face_encodings(unknown_image)
                    if len(file2_encoding) == 0:
                        print("unknown file" + f2 + " was not recognized")
                    else:
                        result = face_recognition.compare_faces([file_encoding], file2_encoding[0])
                        results[origin + f1] = result
                        print(f'{f2} result is {result}')

    return results

    # known_image = face_recognition.load_image_file(f.name)
    # for file2 in os.listdir("../client/captured2"):
    #     if f.endswith(".jpg"):
    #         unknown_image = face_recognition.load_image_file("captured2\\" + file2)
    #         file_encoding = face_recognition.face_encodings(known_image)[0]
    #         file2_encoding = face_recognition.face_encodings(unknown_image)
    #         if len(file2_encoding) == 0:
    #             print("unknown file" + file2 + " was not recognized")
    #         else:
    #             results = face_recognition.compare_faces([file_encoding], file2_encoding[0])
    #             print(results)


@app.route("/", methods=["GET"])
def hello():
    """ Return a friendly HTTP greeting. """
    who = request.args.get("who", "Hi")
    return f"Hello {who}!\n"


if __name__ == "__main__":
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host="localhost", port=8080, debug=True)
