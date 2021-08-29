import face_recognition
import os
import cv2
import smtplib
from email.message import EmailMessage

KNOWN_FACES_DIR = 'caras_conocidas'
# UNKNOWN_FACES_DIR = 'caras_desconocidas'
TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'hog'  # default: 'hog', other one can be 'cnn'

video = cv2.VideoCapture(0)

# Returns (R, G, B) from name
def name_to_color(name):
    color = [(ord(c.lower()) - 97) * 8 for c in name[:3]]
    return color


print('Loading known faces...')
known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):

    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')

        encoding = face_recognition.face_encodings(image)[0]

        known_faces.append(encoding)
        known_names.append(name)

print('Processing video...')

# for filename in os.listdir(UNKNOWN_FACES_DIR):
while True:
    ret, image = video.read()

    # print(f'Filename {filename}', end='')
    # image = face_recognition.load_image_file(f'{UNKNOWN_FACES_DIR}/{filename}')

    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)

    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    print(f', found {len(encodings)} face(s)')
    for face_encoding, face_location in zip(encodings, locations):

        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

        match = None
        if True in results:
            match = known_names[results.index(True)]
            print(f' - {match} from {results}')

            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = name_to_color(match)
            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2] + 22)
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (200, 200, 200), FONT_THICKNESS)

    cv2.imshow(filename, image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        # cv2.waitKey(0)
        cv2.destroyWindow(filename)
        break


def send_mail():
    email_id = os.environ.get("EMAIL_ADDR")
    email_pass = os.environ.get("EMAIL_PASS")

    msg = EmailMessage()
    msg["Subject"] = f"Encontramos a {name}", name
    msg["From"] = email_id
    msg["To"] = "notjoseesquerra@gmail.com"
    msg.set_content("Hola, encontramos a la persona que reportaste como desaparecida")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email_id, email_pass)

        subject = f"Encontramos a {name}", name
        body = "Hola, encontramos a la persona que reportaste como desaparecida"

        msg = f"Subject : {subject}\n\n\n{body}"
        smtp.sendmail(email_id, "notjoseesquerra@gmail.com", msg)
