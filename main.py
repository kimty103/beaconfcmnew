import RPi.GPIO as gpio
import Detect
import Fcm
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

#connect to firebase database
cred = credentials.Certificate("beacon-client-app-firebase-adminsdk-52b5p-186f3fb413.json") #key file name
firebase_admin.initialize_app(cred)

db = firestore.client()

#preprocess to send push message
url = "https://fcm.googleapis.com/fcm/send"
headers = {
  'Authorization': 'key=AAAAFYmlCLM:APA91bFMWQ1z8LQvRn_ffgxx9_CsOwAj4uVhINfwEDxIRdbE254cPkPvjuC3Dxt4adtfEzaVUbIUEAmIjZR7A_dBh2reGklHoZhlcsSSRWeodwBndLjXyxwOpADWI9oIH9CkEpe-Frq2', # key value of firebase project
  'Content-Type': 'application/json'
}

callback_done = threading.Event()

floors_dict = { 1:[], 2:[]}


# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot ,changes, read_time):
    print(u'Callback received query snapshot.')
    print(f"floor :")
    for doc in col_snapshot:
        Fcm.add_dict(doc.id, (doc.to_dict())['floor'])
    callback_done.set()

for i in range(1,3):
    col_query = db.collection(u'workplace').where(u'floor', u'==', i)
    query_watch = col_query.on_snapshot(on_snapshot)
    time.sleep(3)
    db.collection(u'floors').document(str(i)).set({
        'tokens': floors_dict[i]
    })


First_floor = Detect.Floor(1, 17, 0)
Second_floor = Detect.Floor(2, 22, 1)
#Third_floor = Detect.Floor(3, 27, 2)


def process():
    First_floor.fire_detect()
    Second_floor.fire_detect()
    #Third_floor.fire_detect()

    while True:
        time.sleep(3)


if __name__ == '__main__':
    try:
        print("Detect Start")
        process()
    except KeyboardInterrupt:
        print()
        print("End by KeyboardInterrupt!")
        gpio.cleanup()
