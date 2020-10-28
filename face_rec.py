# facial rec

import face_recognition
import os
import cv2


KNOWN_FACES_DIR = "known_faces"
UNKNOWN_FACES_DIR = "unknown_faces"
TOLERANCE = 0.6  # higher leads to false positives
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "cnn"   # convolutional nueral network
# detect a face & every unknown we have to compare with known

print("Loading known faces")

known_faces = []
known_names = []   # to match with known names 

for name in os.listdir(KNOWN_FACES_DIR):
	for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
		image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
		encoding = face_recognition.face_encodings(image)[0]
		known_faces.append(encoding)
		known_faces.append(name)
