import cv2
import mediapipe as mp
import math
import numpy as np
import threading
import time

import pygame

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class HandGesture(threading.Thread):
    def __init__(self):
        super(HandGesture, self).__init__()
        self.volume_thread_stop_event = threading.Event()
        self.pygame_instance = None

    def run(self):
        cam = cv2.VideoCapture(0)

        with mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:

            prev_percentage_gap = 0
            start_time = time.time()

            if self.pygame_instance is None:
                self.pygame_instance = pygame.init()

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
                        if abs(percentage_gap - prev_percentage_gap) > 1.5:
                            per = percentage_gap / 100
                            pygame.mixer.music.set_volume(per)

                        # Mettre à jour le pourcentage précédent
                        prev_percentage_gap = percentage_gap

                # Check elapsed time and stop the thread after 5 seconds
                if time.time() - start_time >= 5:
                    self.volume_thread_stop_event.set()

            cam.release()
