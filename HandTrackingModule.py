import cv2
import mediapipe as mp
import time


class handDetector():
    def __int__(self, mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

                for id, lm in enumerate(handLms.landmark):

                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    print(id, cx, cy)

                    if id == 4:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)

                if id == 4:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (20, 20, 207), 3)

    cv2.imshow("Pantalla de video", img)

    # Esperar 1 milisegundo para detectar si se presiona una tecla
    key = cv2.waitKey(1)

    # Si se presiona 'q' o 'Q', romper el bucle para salir de la aplicación
    if key == ord('q') or key == ord('Q'):
        break

# Liberar recursos y cerrar la ventana
cap.release()
cv2.destroyAllWindows()


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (20, 20, 207), 3)

        cv2.imshow("Pantalla de video", img)

        # Esperar 1 milisegundo para detectar si se presiona una tecla
        key = cv2.waitKey(1)

        # Si se presiona 'q' o 'Q', romper el bucle para salir de la aplicación
        if key == ord('q') or key == ord('Q'):
            break


if __name__ == "__main__":
    main()
