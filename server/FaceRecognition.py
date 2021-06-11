import face_recognition
import os
from flask import escape

import pyrebase

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
path_on_cloud = "bus_xxx/entranceCam/"
files = storage.bucket.list_blobs(path_on_cloud)
for f in files:
    print(f.name)
    firebase.storage().child(f.name).download("cur_im.jpg")


def compare_faces(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # request_json = y
    # .get_json(silent=True)
    # request_args = request.args
    # path_on_cloud = request_args['path_on_cloud']
    # if request_json and 'name' in request_json:
    #     name = request_json['name']
    # elif request_args and 'name' in request_args:
    #     name = request_args['name']
    # else:
    #     name = 'World'
    # return 'Hello {}!'.format(escape(name))

    for f in storage.bucket.list_blobs(path_on_cloud):
        if not f.name.endwith('.jpg'):
            break
        firebase.storage().child(f.name).download(f.name)
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
