import time
import numpy as np
import cv2
import face_recognition
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from CreateSQL_neighbours import Projektas
from datetime import datetime
import speech_recognition as sr

r = sr.Recognizer()

engine = create_engine('sqlite:///neighbordetector.db')
Session = sessionmaker(bind=engine)
session = Session()

path = 'Images'
images = []
classNames = []
myList = os.listdir(path)

for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)

cap = cv2.VideoCapture(0)


# DecetcTime = datetime.now()
# timeFormat = DecetcTime.strftime("%H:%M")
#
# lastTime = []
# guestTime = session.query(Projektas).all()
# for gTime in guestTime:
#     lastTime.append(gTime.time)
#     lastTime.reverse()



def face_identification():
    while True:
        sucess, img = cap.read()
        imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faceFrame = face_recognition.face_locations(imgS)
        encodeFrame = face_recognition.face_encodings(imgS, faceFrame)

        for encodeFace, faceLoc in zip(encodeFrame, faceFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()

                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 10), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 10, y2 + 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                DecetcTime = datetime.now()
                timeFormat = DecetcTime.strftime("%H:%M")

                if name == "MUSK":
                    print('Vartai atrakinti')
                    lastTime = []
                    guestTime = session.query(Projektas).all()
                    for gTime in guestTime:
                        lastTime.append(gTime.time)
                        lastTime.reverse()
                    if lastTime[0] != timeFormat:
                        neighbours = Projektas(name, timeFormat)
                        session.add(neighbours)
                        session.commit()

                else:
                    lastTime = []
                    guestTime = session.query(Projektas).all()
                    for gTime in guestTime:
                        lastTime.append(gTime.time)
                        lastTime.reverse()

                    if lastTime[0] != timeFormat:
                        neighbours = Projektas(name, timeFormat)
                        session.add(neighbours)
                        session.commit()

                    print("Press doorbell")

        cv2.imshow('Cam', img)
        cv2.waitKey(1)

def master():
    while True:
        with sr.Microphone() as source:
            print("Jusu slaptazodis")
            audio = r.listen(source)

            text = r.recognize_google(audio)
            if text == "hello":
                face_identification()
                break
            else:
                print("Bandykite dar karta")

person = input("Guest(1) ---- Master(2)")

if person == "1":
    face_identification()
    time.sleep(10)

if person == "2":
    master()
