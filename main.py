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

getValue = 0
while(1):
    getValue = int(input())   #get input value(this maybe a sensor value)
 #   print(getValue)
    if(getValue == 1):
        users_ref = db.collection(u'workplace')
        docs = users_ref.stream()
        for doc in docs:
            #print(f'{doc.id} => {(doc.to_dict())["token"]}')
            #print((doc.to_dict()))
            msg = "your floor is " + str((doc.to_dict())["floor"])
            payload = json.dumps({
              "to": (doc.to_dict())["token"],
              "notification": {
                "title": "Python",
                "body": msg,
                "image": "https://lh3.googleusercontent.com/pw/AM-JKLUHlrO-HT4yXM2ubElH3wfnwlTYtLIlhaeoGzFw3VIPmRK4p-LjEk0wvD4tM9RQE1t9nO8zyiQXqy55VRlxLqWeWRDIN5SXTH7W2ZAQuPF8H3TykISf_eOLnWN3oY1-EqOpWo_vvvwOj18zh7_QROCz=w653-h870-no?authuser=0"
              },
                "data":{
                    "image": "https://lh3.googleusercontent.com/pw/AM-JKLUHlrO-HT4yXM2ubElH3wfnwlTYtLIlhaeoGzFw3VIPmRK4p-LjEk0wvD4tM9RQE1t9nO8zyiQXqy55VRlxLqWeWRDIN5SXTH7W2ZAQuPF8H3TykISf_eOLnWN3oY1-EqOpWo_vvvwOj18zh7_QROCz=w653-h870-no?authuser=0"
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
        print(type(docs))
    elif(getValue == -1):
        break

