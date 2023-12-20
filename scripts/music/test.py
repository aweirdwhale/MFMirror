import cv2
import threading

import pygame
import numpy as np
import math

import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class volume:

    def __init__(self, window):
        self.volume_thread_stop_event = threading.Event()
        self.window = window


    def Ajust_volume(self):
        cam = cv2.VideoCapture(0)

        with mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:

            prev_percentage_gap = 0

            while not self.volume_thread_stop_event.is_set() and cam.isOpened():
                success, image = cam.read()

                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                lmList = []
                if results.multi_hand_landmarks:
                    myHand = results.multi_hand_landmarks[0]
                    for id, lm in enumerate(myHand.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])

                    if len(lmList) != 0:
                        x1, y1 = lmList[4][1], lmList[4][2]
                        x2, y2 = lmList[8][1], lmList[8][2]

                        length = math.hypot(x2 - x1, y2 - y1)
                        percentage_gap = round(np.interp(length, [50, 220], [0, 100]))

                        # Vérifier si le pourcentage augmente
                        if (percentage_gap - prev_percentage_gap) > 1.5 or (
                                percentage_gap - prev_percentage_gap) < -1.5:
                            per = percentage_gap / 100
                            pygame.mixer.music.set_volume(per)

                            # Mettre à jour le pourcentage précédent
                        prev_percentage_gap = percentage_gap

            cam.release()


    def Stop_volume_adjustment(self):
        self.volume_thread_stop_event.set()


    def start_volume_adjustment(self, duration):
        # Démarrez le thread pour ajuster le volume
        volume_thread = threading.Thread(target=self.Ajust_volume)
        volume_thread.start()

        # Planifiez l'arrêt du thread après un certain délai
        self.window.after(duration, self.Stop_volume_adjustment)



if __name__ == __main__:
    vol = volume("0")
    vol.start_volume_adjustment(10000)

