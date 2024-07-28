import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

# Load the video capture device
video_capture = cv2.VideoCapture(0)

# Load images and create encodings
known_face_encodings = []
known_face_names = ["azam", "Ranjana", "Roshani dafedar", "Sahana", "Roshani Mulla", "vishal", "tata", "jobs", "Mr. RAGHAVENDRA SHEDDI", "tesla"]

# Function to load images and get face encodingsq
def load_and_encode_image(file_path):
    image = face_recognition.load_image_file(file_path)
    return face_recognition.face_encodings(image)[0]

# Load all images
known_face_encodings = [
    load_and_encode_image("photos/azam.jpg"),
    load_and_encode_image("photos/Ranjana.jpg"),
    load_and_encode_image("photos/Roshani_dafedar.jpg"),
    load_and_encode_image("photos/Sahana.jpg"),
    load_and_encode_image("photos/Roshani_Mulla.jpg"),
    load_and_encode_image("photos/vishal.jpg"),
    load_and_encode_image("photos/tata.jpg"),
    load_and_encode_image("photos/jobs.jpg"),
    load_and_encode_image("photos/sir.jpg"),  # Add SHEDDI sir's image
    load_and_encode_image("photos/tesla.jpg")  # Add tesla.jpg
]

students = known_face_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date + '.csv', 'w+', newline='')
lnwriter = csv.writer(f)

while True:
    ret, frame = video_capture.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

    if s:
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            
            # Check if any matches were found
            if True in matches:
                best_match_index = np.argmin(face_distances)
                name = known_face_names[best_match_index]

                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = datetime.now().strftime("%H-%M-%S")
                    lnwriter.writerow([name, current_time])
            face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Attendance System', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
f.close()
