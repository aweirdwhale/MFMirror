#!/usr/bin/env python3

import time

import cv2
import imutils
from imutils import paths
import numpy as np
import os
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from imutils.video import FPS

percent = 0


class FaceRecognition:
    def __init__(self, cameraIndex):
        self.cameraIndex = int(cameraIndex)
        self.dataset = '/home/aweirdwhale/Bureau/Aweirdwhale/Miroir/mfm/scripts/face_recon/dataset'
        self.embeddings = '/home/aweirdwhale/Bureau/Aweirdwhale/Miroir/mfm/scripts/face_recon/output/embeddings.pickle'
        self.recognizer = '/home/aweirdwhale/Bureau/Aweirdwhale/Miroir/mfm/scripts/face_recon/output/recognizer.pickle'
        self.le = '/home/aweirdwhale/Bureau/Aweirdwhale/Miroir/mfm/scripts/face_recon/output/le.pickle'
        self.protopath = "/home/aweirdwhale/Bureau/Aweirdwhale/Miroir/mfm/scripts/face_recon/face_detection_model/deploy.prototxt"
        self.deploypath = "/home/aweirdwhale/Bureau/Aweirdwhale/Miroir/mfm/scripts/face_recon/face_detection_model/deploy.prototxt"  # Why the fuck do I have to put the absolute path???
        self.modelpath = "/home/aweirdwhale/Bureau/Aweirdwhale/Miroir/mfm/scripts/face_recon/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
        self.detector = cv2.dnn.readNetFromCaffe(self.protopath, self.modelpath)
        self.embedder = cv2.dnn.readNetFromTorch("/home/aweirdwhale/Bureau/Aweirdwhale/Miroir/mfm/scripts/face_recon/openface_nn4.small2.v1.t7")
        self.knownEmbeddings = []
        self.knownNames = []
        self.total = 0

    def extract(self):
        print("Loading Face Detection Model...")
        print("Quantifying Faces...")
        imagePaths = list(paths.list_images(self.dataset))

        for (i, imagePath) in enumerate(imagePaths):
            if i % 50 == 0:
                print("Processing image {}/{}".format(i, len(imagePaths)))

            name = imagePath.split(os.path.sep)[-2]
            image = cv2.imread(imagePath)
            image = imutils.resize(image, width=600)
            (h, w) = image.shape[:2]

            imageBlob = cv2.dnn.blobFromImage(
                cv2.resize(image, (300, 300)), 1.0, (300, 300),
                (104.0, 177.0, 123.0), swapRB=False, crop=False)

            self.detector.setInput(imageBlob)
            detections = self.detector.forward()

            if len(detections) > 0:
                i = np.argmax(detections[0, 0, :, 2])
                confidence = detections[0, 0, i, 2]

                if confidence > 0.5:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    face = image[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]

                    if fW < 20 or fH < 20:
                        continue

                    faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                                     (96, 96), (0, 0, 0), swapRB=True, crop=False)
                    self.embedder.setInput(faceBlob)
                    vec = self.embedder.forward()

                    self.knownNames.append(name)
                    self.knownEmbeddings.append(vec.flatten())
                    self.total += 1

        print("[INFO] Serializing {} encodings...".format(self.total))
        data = {"embeddings": self.knownEmbeddings, "names": self.knownNames}
        with open(self.embeddings, "wb") as f:
            f.write(pickle.dumps(data))

        print("[INFO] Done")

    def create_directory(self, username):
        """
        Create a directory for the user.
        """
        directory = username
        path = os.path.join(self.dataset, directory)

        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print(f"Directory '{path}' created successfully.")
            except OSError as e:
                print(f"Error creating directory '{path}': {e}")
        else:
            print(f"Directory '{path}' already exists.")

    def implement_dataset(self, username):
        """
        Implement the dataset for face recognition.
        """

        directory = username
        path = os.path.join(self.dataset, directory)

        self.create_directory(username)

        cap = cv2.VideoCapture(self.cameraIndex)

        for i in range(1, 61):
            ret, frame = cap.read()
            cv2.imwrite(f"{path}/{i}.png", frame)

            percent_done = round((i / 60) * 100)
            done = round(percent_done / (100 / 60))
            togo = 60 - done
            done_str = '█' * int(done)
            togo_str = '░' * int(togo)

            print(f'\t⏳ Implementing dataset: [{done_str}{togo_str}] {percent_done}% done', end='\r')

            time.sleep(0.2)

            cv2.waitKey(1)

        print(f'\t✅ Implementing dataset: [DONE]')
        cap.release()
        cv2.destroyAllWindows()

    def train(self):
        # dump the facial embeddings + names to disk
        print("[INFO] serializing {} encodings...".format(self.total))
        data = {"embeddings": self.knownEmbeddings, "names": self.knownNames}
        f = open(self.embeddings, "wb")
        f.write(pickle.dumps(data))
        f.close()

        print("[INFO] Done")

        # Load face embeddings
        print("[INFO] loading embeds...")
        data = pickle.loads(open(self.embeddings, "rb").read())

        # encode the labels
        print("[INFO] encoding labels...")
        le = LabelEncoder()
        labels = le.fit_transform(data["names"])

        # train the model used to accept the 128-d embeddings of the face and
        # then produce the actual face recognition
        print("[INFO] training model...")
        recognizer = SVC(C=1.0, kernel="linear", probability=True)
        recognizer.fit(data["embeddings"], labels)

        # write the actual face recognition model to disk
        f = open(self.recognizer, "wb")
        f.write(pickle.dumps(recognizer))
        f.close()

        # write the label encoder to disk
        f = open(self.le, "wb")
        f.write(pickle.dumps(le))
        f.close()

        print('[INFO] model trained !')

    def recognition(self):
        # Load the serialized face detector
        global percent
        print("Loading face detector...")

        detector = cv2.dnn.readNetFromCaffe(self.deploypath, self.modelpath)

        # Load the serialized face feature extractor model
        print("Loading face recognizer...")
        extractor = self.embedder

        # Load the actual face recognition model along with the label encoder
        recognizer = pickle.loads(open(self.recognizer, "rb").read())
        le = pickle.loads(open(self.le, "rb").read())

        # Initialize video capture from the default camera (index 0)
        cap = cv2.VideoCapture(self.cameraIndex)

        # Start the Frames Per Second (FPS) estimator
        fps = FPS().start()
        name = None
        proba = 0

        img_counter = 0

        print("recognition started")
        # Loop over the frames from the video stream
        while True:
            # Capture the frame from the camera
            _, frame = cap.read()

            if not _:
                print("failed to grab frame")
                break
            # Resize the frame to have a width of 600 pixels (maintaining the aspect ratio),
            # then get the dimensions of the frame
            frame = imutils.resize(frame, width=600)
            (h, w) = frame.shape[:2]

            # Construct a blob from the frame
            blobImage = cv2.dnn.blobFromImage(
                cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                (104.0, 177.0, 123.0), swapRB=False, crop=False
            )

            # Apply the deep learning-based face detector to localize faces in the input image
            detector.setInput(blobImage)
            detections = detector.forward()

            # Loop over the detections
            for i in range(0, detections.shape[2]):
                # Extract the confidence associated with the prediction
                confidence = detections[0, 0, i, 2]

                # Filter out weak detections
                if confidence > 0.5:
                    # Calculate the (x, y)-coordinates of the bounding box for the face
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # Extract the face ROI
                    face = frame[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]

                    # Ensure the face width and height are sufficiently large
                    if fW < 20 or fH < 20:
                        continue

                    # Construct a blob for the face ROI, then pass the blob through our face feature extractor model to
                    # obtain the 128-d quantification of the face
                    blobFace = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
                    extractor.setInput(blobFace)
                    vec = extractor.forward()

                    # Perform classification to recognize the face
                    predictions = recognizer.predict_proba(vec)[0]
                    j = np.argmax(predictions)
                    proba = predictions[j]
                    name = le.classes_[j]

                    percent = round(proba * 100)

            if proba > 0.8:
                if name is not None and name != "unknown":
                    return name, percent

                elif name == "unknown":
                    pass

        # clean up
        cap.release()
    # Rest of the code remains unchanged


if __name__ == "__main__":
    face_recognition = FaceRecognition(cameraIndex=0)
    # face_recognition.implement_dataset(username='test')
    face_recognition.extract()
    face_recognition.train()
    print(face_recognition.recognition())
