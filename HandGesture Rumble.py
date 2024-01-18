import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = HandDetector(maxHands=1)
timer = 0
stateResult = False
startGame = False
scores = [0, 0]

while True:
    imgBG = cv2.imread(r"C:\Users\user\Desktop\Games\BG.png")
    success, img = cap.read()
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:477]
    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
            if timer > 3:
                stateResult = True
                timer = 0
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
                    # Check if the image is loaded successfully
                    # if imgAI is not None:
                     

                    if (playerMove == 1 and randomNumber == 3) or \
                                (playerMove == 2 and randomNumber == 1) or \
                                (playerMove == 3 and randomNumber == 2):
                                    scores[1] += 1  # AI win
                    

                    if (playerMove == 3 and randomNumber == 1) or \
                                (playerMove == 1 and randomNumber == 2) or \
                                (playerMove == 2 and randomNumber == 3):
                                    scores[0] += 1

    imgBG[234:654, 796:1193] = imgScaled
    if stateResult and imgAI is not None:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (225, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (225, 255, 255), 6)
    # if sum(scores) == 5:
    #     if scores[0] > scores[1]:
    #         cv2.putText(imgBG, 'AI Wins', (550, 405), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    #     else:
    #         cv2.putText(imgBG, 'Player Wins', (550, 405), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.imshow("BG", imgBG)
    key = cv2.waitKey(1)

    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
     
      # Exit key
    if key == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
