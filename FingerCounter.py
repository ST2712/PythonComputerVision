import cv2
import time
import os
import HandTrackingModule as htm

# Configuración de las dimensiones de la ventana de captura de la cámara
wCam, hCam = 1280, 720

# Inicialización de la captura de video con la cámara predeterminada
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Establecer la anchura de la ventana de captura
cap.set(4, hCam)  # Establecer la altura de la ventana de captura

# Directorio donde se encuentran las imágenes a superponer
folderPath = "FingerImages"
myList = os.listdir(folderPath)  # Lista de archivos en el directorio
# print(myList)  # Imprimir la lista de imágenes

# Inicializar una lista para almacenar las imágenes de superposición
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')  # Leer cada imagen
    print(f'{folderPath}/{imPath}')  # Imprimir la ruta de cada imagen
    overlayList.append(image)  # Añadir la imagen a la lista de superposición

# print(len(overlayList))  # Imprimir la cantidad de imágenes cargadas

# Variables para calcular y mostrar los fotogramas por segundo (FPS)
pTime = 0

# Crear una instancia del detector de manos con una confianza de detección y un máximo de manos a detectar
detector = htm.handDetector(detectionCon=0.75, maxHands=1)

# Índices de las puntas de los dedos en la lista de marcas de la mano
tipIds = [4, 8, 12, 16, 20]

# Bucle principal para la captura continua de video
while True:
    success, img = cap.read()  # Leer un fotograma de la cámara
    img = detector.findHands(img)  # Detectar y dibujar las manos en el fotograma
    img = cv2.flip(img, 1) # Girar la imagen para evitar el modo espejo
    lmList = detector.findPosition(img, draw=False)  # Obtener la posición de las marcas de la mano

    # Si se encontraron marcas de la mano en la imagen
    if len(lmList) != 0:
        fingers = []
        # Comprobar el pulgar
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)  # Pulgar visible/levantado
        else:
            fingers.append(0)  # Pulgar no visible/bajado

        # Comprobar los otros cuatro dedos
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)  # Dedo levantado
            else:
                fingers.append(0)  # Dedo bajado

        # Contar el total de dedos levantados
        totalFingers = fingers.count(1)
        print(totalFingers)

        # Seleccionar la imagen de superposición basada en el número de dedos levantados
        if totalFingers == 0:
            overlayImg = overlayList[0]  # Si no hay dedos levantados, seleccionar la primera imagen
        elif totalFingers < len(overlayList):
            overlayImg = overlayList[totalFingers]  # Seleccionar imagen correspondiente al número de dedos
        else:
            overlayImg = overlayList[-1]  # Si el número excede las imágenes disponibles, usar la última

        # Obtener las dimensiones de la imagen de superposición y aplicarla en el fotograma de la cámara
        h, w, c = overlayImg.shape
        img[0:h, 0:w] = overlayImg

        # Dibujar un rectángulo y mostrar el número total de dedos levantados
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    # Calcular y mostrar los FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    # Mostrar el fotograma en una ventana
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    # Si se presiona 'q' o 'Q', romper el bucle para salir de la aplicación
    if key == ord('q') or key == ord('Q'):
        break

# Liberar la cámara y cerrar todas las ventanas abiertas por OpenCV
cap.release()
cv2.destroyAllWindows()
