from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import numpy as np
import time
import requests
import contextlib
from ultralytics import YOLO
import pygame
#from pushbullet import Pushbullet


class Detection(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, token, location, receiver):
        super(Detection, self).__init__()
        self.token = token
        self.location = location
        self.receiver = receiver
        self.running = True
        self.model = YOLO("weights/n_best.pt")

        # Alarm and notification setup
        pygame.mixer.init()
        self.alarm_playing = False
        #self.pb = Pushbullet("o.bpldsldStXfpnqQJzAVZiZIAT8HCJGBw")  # Replace this with your Pushbullet token
        self.last_alert_time = 0

    def run(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue

            detected = False
            with contextlib.redirect_stdout(None):
                results = self.model(frame, conf=0.80, verbose=False)

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]

                    if class_name == "Handgun" and confidence > 0.80:
                        detected = True
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(frame, f"{class_name} {confidence:.2%}", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                        if time.time() - self.last_alert_time >= 10:
                            self.save_detection(frame)
                            self.last_alert_time = time.time()

            if detected:
                self.play_alarm()
            else:
                self.stop_alarm()
                #print("No weapon detected")

            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, frame.shape[1], frame.shape[0],
                                       3 * frame.shape[1], QImage.Format_RGB888)
            scaledImage = convertToQtFormat.scaled(854, 680, Qt.KeepAspectRatio)
            self.changePixmap.emit(scaledImage)

        cap.release()
        self.stop_alarm()

    def save_detection(self, frame):
        """ Save frame and trigger alert """
        cv2.imwrite("saved_frame/frame.jpg", frame)
        #print('📸 Frame saved')
        self.post_detection()
       # self.send_push_notification("🚨 Weapon Detected", f"Location: {self.location}")

    def post_detection(self):
        """ Send image + info to Django server """
        try:
            url = 'http://127.0.0.1:8000/api/images/'
            headers = {'Authorization': 'Token ' + self.token}
            files = {'image': open('saved_frame/frame.jpg', 'rb')}
            data = {'user_ID': self.token, 'location': self.location, 'alert_receiver': self.receiver}
            response = requests.post(url, files=files, headers=headers, data=data)

            if response.ok:
                print('🚨 Alert sent to the user')
            else:
                print('❌ Server alert failed')
        except Exception as e:
            print('❌ Error contacting server:', e)

    def play_alarm(self):
        """ Start alarm if not already playing """
        if not self.alarm_playing:
            pygame.mixer.music.load("alarms/alarm.mp3")
            pygame.mixer.music.play(-1)
            self.alarm_playing = True
            print("🔊 Alarm playing...Weapon Detected")

    def stop_alarm(self):
        """ Stop alarm if it's playing """
        if self.alarm_playing:
            pygame.mixer.music.stop()
            self.alarm_playing = False
            print("🔕 Alarm stopped")

    """def send_push_notification(self, title, message):
        try:
            self.pb.push_note(title, message)
            #print("📱 Push notification sent")
        except Exception as e:
            print("❌ Push notification error:", e) """
