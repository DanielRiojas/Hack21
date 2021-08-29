import face_recognition
import os
import cv2

KNOWN_FACES_DIR = "caras_conocidas"
UNKNOWN_FACES_DIR = "caras_desconocidas"

TOLERANCE = 0.5

FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog"  # cnn/hog

# Returns (R, G, B) from name
def name_to_color(name):
    # Take 3 first letters, tolower()
    # lowercased character ord() value rage is 97 to 122, substract 97, multiply by 8
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color


print('Cargando caras registradas...')
known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

print("Cargando caras desconocidas...")

for filename in os.listdir(UNKNOWN_FACES_DIR):

    print(f'Filename {filename}', end='')
    image = face_recognition.load_image_file(f'{UNKNOWN_FACES_DIR}/{filename}')

    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # turns colors of the image to bgr because thats what CV2 uses

    print(f'Se detecta {len(encodings)} cara(s)')
    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        match = None
        if any(results):
            match = known_names[results.index(True)]
            print(f"Se detectó a: {match}")

            top_left = (face_location[3], face_location[0])
            bot_right = (face_location[1], face_location[2])

            color = name_to_color(match)
            # color = [0, 255, 0]
            cv2.rectangle(image, top_left, bot_right, color, FRAME_THICKNESS)

            top_left = (face_location[3], face_location[2])
            bot_right = (face_location[1], face_location[2]+22)

            cv2.rectangle(image, top_left, bot_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

    cv2.imshow(filename, image)
    cv2.waitKey(0)
    cv2.destroyWindow(filename)
