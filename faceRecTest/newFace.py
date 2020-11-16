#this file tests image recognition by comparing 
#1) A picture of bill gates to a picture of bill gates rendering true
#2) A picutre of bill gates to a picture of obama rendering false
import face_recognition
known_image = face_recognition.load_image_file("billSource.jpg")
unknown_image = face_recognition.load_image_file("billFace.jpg")

#testing bill gates vs. bill gates
konwn_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([konwn_encoding], unknown_encoding)

print(results)

#testing obama vs. obama
unknown_image = face_recognition.load_image_file("obamaFace.jpg")

unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([konwn_encoding], unknown_encoding)

print(results)



