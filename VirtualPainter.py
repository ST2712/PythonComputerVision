import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

brushTickness = 15
eraserTickness = 100
folderPath = "HeaderImages"
myList = os.listdir(folderPath)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[0]

# Definicion de los colores a usar
magenta = (100, 51, 255)
cian = (255, 255, 51)
yellow = (0, 176, 255)
eraser = (0, 0, 0)

drawColor = magenta

# Configuración de las dimensiones de la ventana de captura de la cámara
wCam, hCam = 1280, 720

# Inicialización de la captura de video con la cámara predeterminada
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Establecer la anchura de la ventana de captura
cap.set(4, hCam)  # Establecer la altura de la ventana de captura

detector = htm.handDetector(detectionCon=0.85, maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # 1. Importar la imagenen
    success, img = cap.read()

    # 2. Econtrar los puntos de referencia de las manos
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        xp, yp = 0, 0
        # print(lmList)

        # Dedo indice
        x1, y1 = lmList[8][1:]

        # Dedo corazon
        x2, y2 = lmList[12][1:]

        # 3. Verificar que dedos estan levantados
        fingers = detector.fingersUp()
        #print(fingers)

        # 4. Verificar si el metodo de seleccion esta activado - 2 dedos arriba

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Selection mode")
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = magenta
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = cian
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = yellow
                elif 1050 < x1 < 1250:
                    header = overlayList[3]
                    drawColor = eraser
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. Verificar modo dibujo - el dedo indice está levantado
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == eraser:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserTickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserTickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushTickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushTickness)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Imagen del header por defecto
    img[0:125,0:1280] = header
    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    #cv2.imshow("Inv", imgInv)
    key = cv2.waitKey(1)
    # Si se presiona 'q' o 'Q', romper el bucle para salir de la aplicación
    if key == ord('q') or key == ord('Q'):
        break


