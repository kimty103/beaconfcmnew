import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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

image_evac = [
'https://firebasestorage.googleapis.com/v0/b/beacon-client-app.appspot.com/o/evacuation_1.png?alt=media&token=2dafbbfd-96dd-4b8a-b620-3df0d875f696',
    'https://firebasestorage.googleapis.com/v0/b/beacon-client-app.appspot.com/o/evacuation_2.png?alt=media&token=f8d942f7-d5d2-4e10-89f0-07d50bad7f12'
]

getValue = 0
while(1):
    getValue = int(input())   #get input value(this maybe a sensor value)
 #   print(getValue)
    if(getValue == 1):
        users_ref = db.collection(u'workplace4')
        docs = users_ref.stream()
        for doc in docs:
            #print(f'{doc.id} => {(doc.to_dict())["token"]}')
            #print((doc.to_dict()))
            msg = "your floor is " + str((doc.to_dict())["floor"])
            payload = json.dumps({
                "to": (doc.to_dict())["token"],
              #   "notification": {
              #       "title": "Python",
              #       "body": msg,
              #       "click_action": "EmergencyActivity",
              #       # "icon" : "ic_flame",
              #       "color" : "#FF0000",
              #       "image": "https://firebasestorage.googleapis.com/v0/b/beacon-client-app.appspot.com/o/ic_flame.png?alt=media&token=dd90dfa2-303a-42c9-9e8c-3dfa071f2088"
              #
              # },
                "data":{
                    "image": image_evac[(doc.to_dict())["floor"] -1],
                    # "floor": (doc.to_dict())["floor"],
                    "floor": 15,
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
        print(type(docs))
    elif(getValue == -1):
        break

