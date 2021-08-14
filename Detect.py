import RPi.GPIO as gpio
import time
import datetime
import firebase_admin
import Fcm
import requests
import json
import spidev as spi
from firebase_admin import credentials
from firebase_admin import firestore
import threading

cred = credentials.Certificate("beacon-client-app-firebase-adminsdk-52b5p-186f3fb413.json") #key file name
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'FireState').document(u'Sensors')

spi = spi.SpiDev()
spi.open(0, 0)

class FlameSensor:
    def __init__(self, pin):
        self.pin = pin
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin, gpio.IN, pull_up_down=gpio.PUD_UP)


class MQ2Sensor:
    def __init__(self, ch_num):
        self.chNum = ch_num

    def read_adc(self):
        if self.chNum > 7 or self.chNum < 0:
            return -1
        buff = spi.xfer2([6 | (self.chNum & 4) >> 2, (self.chNum & 3) << 6, 0])
        adc_value = ((buff[1] & 15) << 8) + buff[2]
        return adc_value

    def gas(self):
        mq2 = self.read_adc()
        print(f"gas : {mq2}")
        return mq2


class Floor:
    def __init__(self, floor: int, flame_pin: int, ch_num: int):
        self.floor = floor
        self.mq2Sensor = MQ2Sensor(ch_num)
        self.flameSensor = FlameSensor(flame_pin)
        self.gasStandard = 200  # 가스 센서 통해 실험 해보고 값 변경할 것.

    def calc_time(self):
        now = datetime.datetime.now()
        date = now.strftime("%Y/%m/%d %H:%M")
        return date

    def send_message_to_firebase(self):
        date = self.calc_time()

        if self.mq2Sensor.gas() > self.gasStandard:
            print(f'Fire detected on {self.floor} floor')
            Fcm.sendFcm()
            doc_ref.set({
                u'Time': date,
                u'Floor': self.floor,
                u'FireDetected': u'TRUE'
            })
        else:
            doc_ref.set({
                u'Time': date,
                u'Floor': self.floor,
                u'FireDetected': u'FALSE'
            })

    def fire_detect(self):
        gpio.add_event_detect(self.flameSensor.pin, gpio.RISING, callback=lambda x: self.send_message_to_firebase(),
                              bouncetime=50)




def process():
    First_floor.fire_detect()
    Second_floor.fire_detect()
    #Third_floor.fire_detect()

    while True:
        time.sleep(3)


