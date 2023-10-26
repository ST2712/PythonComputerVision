import cv2
import time
import numpy as np

##########################
wCam, hCam = 1280, 720
##########################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

while True:
    success, img = cap.read()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 1,
                (255, 0, 0), 3)

    cv2.imshow("Pantalla de video", img)
    cv2.moveWindow('Pantalla de video', 150, 50)

    key = cv2.waitKey(1)

    # Si se presiona 'q' o 'Q', romper el bucle para salir de la aplicación
    if key == ord('q') or key == ord('Q'):
        break

# Liberar recursos y cerrar la ventana
cap.release()
cv2.destroyAllWindows()