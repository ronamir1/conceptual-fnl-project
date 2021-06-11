from flask import Flask, request
import os
import pyrebase
import face_recognition

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


# path_on_cloud = "bus_xxx/entranceCam/"
# files = storage.bucket.list_blobs(path_on_cloud)
# for f in files:
#     print(f.name)
#     firebase.storage().child(f.name).download("cur_im.jpg")

@app.route("/compare", methods=["POST"])
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
    origin = request.args.get("origin")
    dest = request.args.get("dest")
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    for f in storage.bucket.list_blobs(prefix=origin):
        if not f.name.endwith('.jpg'):
            break
        firebase.storage().child(f.name).download(f.name)
    for f in storage.bucket.list_blobs(prefix=dest):
        if not f.name.endwith('.jpg'):
            break
        firebase.storage().child(f.name).download(f.name)
    results = {}
    for file in os.listdir(origin):
        if file.endswith(".jpg"):
            known_image = face_recognition.load_image_file(origin + file)
            for file2 in os.listdir(dest):
                if file.endswith(".jpg"):
                    unknown_image = face_recognition.load_image_file(dest + file2)
                    file_encoding = face_recognition.face_encodings(known_image)[0]
                    file2_encoding = face_recognition.face_encodings(unknown_image)
                    if len(file2_encoding) == 0:
                        print("unknown file" + file2 + " was not recognized")
                    else:
                        result = face_recognition.compare_faces([file_encoding], file2_encoding[0])
                        results[origin + file] = result
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
