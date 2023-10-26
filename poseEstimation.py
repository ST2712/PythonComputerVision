import time
import cv2
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

#cap = cv2.VideoCapture("videos/video2.mp4")
cap = cv2.VideoCapture(0)

new_width = 640
new_height = 480

pTime = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (new_width, new_height))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            print(id, lm)
            cx, cy = int(lm.x*w), int(lm.y*h)

            if id == 0:
                cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255,0,0),3)

    cv2.imshow("Pantalla de video", img)
    cv2.moveWindow('Pantalla de video', 450, 150)

    # Esperar 1 milisegundo para detectar si se presiona una tecla
    key = cv2.waitKey(1)

    # Si se presiona 'q' o 'Q', romper el bucle para salir de la aplicación
    if key == ord('q') or key == ord('Q'):
        break

# Liberar recursos y cerrar la ventana
cap.release()
cv2.destroyAllWindows()