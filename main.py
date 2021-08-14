import requests
import json
import firebase_admin
import threading
import time
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

# Create an Event for notifying main thread.
callback_done = threading.Event()

floors_dict = { 1:[], 2:[],3:[]}

# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot ,changes, read_time):
    print(u'Callback received query snapshot.')
    print(f"floor :")
    for doc in col_snapshot:
        add_dict(doc.id,(doc.to_dict())['floor'])
    print(floors_dict)
    callback_done.set()

def add_dict (to_add, floor):
    for num,floors in floors_dict.items():
        if(num != floor and to_add in floors):
            floors.remove(to_add)
            floors_dict[num] = floors
            db.collection(u'floors').document(str(floor)).set({
                'tokens' : floors_dict[num]
            })
        elif(num == floor and to_add in floors):
            return

        elif(num == floor and to_add not in floors):
            floors_dict[floor].append(to_add)
            db.collection(u'floors').document(str(floor)).set({
                'tokens' : floors_dict[floor]
            })

for i in range(1,4):
    col_query = db.collection(u'workplace').where(u'floor', u'==', i)
    query_watch = col_query.on_snapshot(on_snapshot)

    time.sleep(3)
    print(f'floor {i} : {floors_dict[i]}')
    db.collection(u'floors').document(str(i)).set({
        'tokens' : floors_dict[i]
    })

# Watch the collection query

getValue = 0
#while(1):
#    getValue = int(input())   #get input value(this maybe a sensor value)
 #   print(getValue)
#    if(getValue == 1):
#        users_ref = db.collection(u'workplace')
#        docs = users_ref.stream()
#        for doc in docs:
#            if((doc.to_dict())["enter"]):
#                print(f'{(doc.to_dict())["token"]} = {(doc.to_dict())["enter"]}')
#                #print((doc.to_dict()))
#                msg = "your floor is " + str((doc.to_dict())["floor"])
#                payload = json.dumps({
#                  "to": (doc.to_dict())["token"],
#                  "notification": {
#                    "title": "Warning!!!",
#                    "body": "fire in the building!!!!",
#                    "image": "https://us.123rf.com/450wm/yehorlisnyi/yehorlisnyi1610/yehorlisnyi161000137/64114511-%EA%B2%A9%EB%A6%AC-%EB%90%9C-%EC%B6%94%EC%83%81-%EB%B6%89%EC%9D%80-%EC%83%89%EA%B3%BC-%EC%98%A4%EB%A0%8C%EC%A7%80%EC%83%89-%ED%99%94%EC%9E%AC-%EB%B6%88%EA%BD%83-%ED%9D%B0%EC%83%89-%EB%B0%B0%EA%B2%BD%EC%97%90-%EC%84%A4%EC%A0%95-%EC%BA%A0%ED%94%84-%ED%8C%8C%EC%9D%B4%EC%96%B4-%EB%A7%A4%EC%9A%B4-%EC%9D%8C%EC%8B%9D-%EA%B8%B0%ED%98%B8%EC%9E%85%EB%8B%88%EB%8B%A4-%EC%97%B4-%EC%95%84%EC%9D%B4%EC%BD%98%EC%9E%85%EB%8B%88%EB%8B%A4-%EB%9C%A8%EA%B1%B0%EC%9A%B4-%EC%97%90%EB%84%88%EC%A7%80-%EA%B8%B0%ED%98%B8%EC%9E%85%EB%8B%88%EB%8B%A4-%EB%B2%A1%ED%84%B0-%ED%99%94%EC%9E%AC-%EA%B7%B8%EB%A6%BC%EC%9E%85%EB%8B%88%EB%8B%A4-.jpg?ver=6"
#                  },
#                    "data":{
#                        "floor" : (doc.to_dict())['floor']
#                    }
#                })
#                response = requests.request("POST", url, headers=headers, data=payload)
#                print(response.text)
#        print(type(docs))
#    elif(getValue == -1):
#        break

