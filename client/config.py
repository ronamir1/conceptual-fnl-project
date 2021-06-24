import pyrebase

config = {"apiKey": "AIzaSyCM1MwSxh3NGOJ5MuumUcRmlZKs_b5Sp0g",
          "authDomain": "inspectorapp-6d1d7.firebaseapp.com",
          "databaseURL": "https://inspectorapp-6d1d7.firebaseapp.com",
          "projectId": "inspectorapp-6d1d7",
          "storageBucket": "inspectorapp-6d1d7.appspot.com",
          "messagingSenderId": "1093381045628",
          "appId": "1:1093381045628:web:061bf8752b2bff363538f9",
          "measurementId": "G-33MMBH01LN"}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
bus_id = "bus_xxx"
cam_type = 'entranceCam'
xml_path = r"../xmls/haarcascade_frontalface_default.xml"
BASE_API = r'https://inspector-service-354e3fpima-ew.a.run.app'
