import cv2
import face_recognition

if __name__ == '__main__':

    # Load the cascade

    # To capture video from webcam.
    cap = cv2.VideoCapture(0)
    # To use a video file as input
    # cap = cv2.VideoCapture('filename.mp4')
    face_cascade = cv2.CascadeClassifier("C:\\Users\\Ron\\anaconda3\\envs\\tf-gpu\\Library\\etc\haarcascades\\haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier('C:\\Users\Ron\\anaconda3\envs\\tf-gpu\\Library\\etc\\haarcascades\\haarcascade_eye.xml')

    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi = img[y:y + h, x:x + w]
        # Display
            cv2.imwrite(f"captured2\\person_{i}.jpg", roi)
        cv2.imshow('img', img)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    # Release the VideoCapture object
    cap.release()
