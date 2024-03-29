import cv2
import numpy as np
import face_recognition

def detect_fake_picture(dm,img):
   
    average_color = np.average(img, axis=(0, 1))
    if np.any(average_color < 50) or np.any(average_color > 200):
        return "Fake - Strange colors detected"

    
    edges = cv2.Canny(img, 100, 200)
    if np.mean(edges) > 10:
        return "Fake - Jagged edges detected"

  
    if np.sum(np.abs(np.diff(img, axis=0))) < 1000:
        return "Fake - Strange patterns detected"

    # If none of the rules triggered, it's likely real
    return "Real - No signs of fakeness detected"


Dhatri_image = face_recognition.load_image_file("Dhatri.jpg")
Dhatri_face_encoding = face_recognition.face_encodings(Dhatri_image)[0]

Sirisha_image = face_recognition.load_image_file("Sirisha.jpg")
Sirisha_face_encoding = face_recognition.face_encodings(Sirisha_image)[0]

known_face_encodings = [
    Dhatri_face_encoding, Sirisha_face_encoding
]
known_face_names = [
    "Dhatri", "Sirisha"
]


video_capture = cv2.VideoCapture(0)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()

    # Fake ID detection
    fake_id_result = detect_fake_picture(ret,frame)
    print()

    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        # Facial recognition
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,
face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings,
face_encoding,tolerance=0.5)
            name = "Unknown"

            face_distances =
face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name+fake_id_result)
    #
    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0,
255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255,
255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

