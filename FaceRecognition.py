import face_recognition
import os
if __name__ == '__main__':

    for file in os.listdir("captured"):
        if file.endswith(".jpg"):
            known_image = face_recognition.load_image_file("captured\\" + file)
            for file2 in os.listdir("captured2"):
                if file.endswith(".jpg"):
                    unknown_image = face_recognition.load_image_file("captured2\\" + file2)
                    file_encoding = face_recognition.face_encodings(known_image)[0]
                    file2_encoding = face_recognition.face_encodings(unknown_image)
                    if len(file2_encoding) == 0:
                        print("unknown file" + file2 + " was not recognized")
                    else:
                        results = face_recognition.compare_faces([file_encoding], file2_encoding[0])
                        print(results)