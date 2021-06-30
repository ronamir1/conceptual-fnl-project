import pyrebase
import os
from dotenv import load_dotenv

load_dotenv('.env')

config = {"apiKey": os.environ['API_KEY'],
          "authDomain": os.environ['AUTH_DOMAIN'],
          "databaseURL": os.environ['DATABASE_URL'],
          "projectId": os.environ['PROJECT_ID'],
          "storageBucket": os.environ['STORAGE_BUCKET'],
          "messagingSenderId": os.environ['MESSAGING_SENDER_ID'],
          "appId": os.environ['APP_ID'],
          "serviceAccount": os.environ['SERVICE_ACOUNT'],
          "measurementId": os.environ['MEASURMENT_ID']}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
bus_id = os.environ['BUS_ID']
index = os.environ['INDEX']
cam_type = os.environ['CAM_TYPE']
xml_path = os.environ['XML_PATH']
BASE_API = os.environ['BASE_API']
