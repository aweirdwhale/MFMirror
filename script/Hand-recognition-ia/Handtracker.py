#Import libs
#libs
import cv2
import mediapipe as mp
import time

#mediapipe init
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

#access to webcam
cap = cv2.VideoCapture(0)
hands = mphands.Hands()

pTime = 0
while True:
    data, img = cap.read()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    #Flip the image (selfie view)
    image = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)

    cv2.putText(img,
                str(int(fps)), #text
                (10,70), #position
                cv2.FONT_HERSHEY_PLAIN, #font
                3, #font size
                (255,0,0), #color
                3) #thickness

    
    #storing the results
    results = hands.process(image)
    
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, 
                hand_landmarks, mphands.HAND_CONNECTIONS)
    cv2.imshow('Hand Tracking Test', image)
    #exit
    if cv2.waitKey(1) == ord('q'):
        break