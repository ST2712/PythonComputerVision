import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

folderPath = "HeaderImages"
myList = os.listdir(folderPath)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[0]

# Configuración de las dimensiones de la ventana de captura de la cámara
wCam, hCam = 1280, 720

# Inicialización de la captura de video con la cámara predeterminada
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Establecer la anchura de la ventana de captura
cap.set(4, hCam)  # Establecer la altura de la ventana de captura

detector = htm.handDetector(detectionCon=0.85)

while True:
    # 1. Importar la imagenen
    success, img = cap.read()

    # 2. Econtrar los puntos de referencia de las manos
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)

        # Dedo indice
        x1, y1 = lmList[8][1:]

        # Dedo corazon
        x2, y2 = lmList[12][1:]

        # 3. Verificar que dedos estan levantados
        fingers = detector.fingersUp()
        print(fingers)

    # 4. Verificar si el metodo de seleccion esta activado - 2 dedos arriba

    # 5. Verificar modo dibujo - el dedo indice está levantado



    # Imagen del header por defecto
    img[0:125,0:1280] = header

    cv2.imshow("Image", img)
    cv2.waitKey(1)


