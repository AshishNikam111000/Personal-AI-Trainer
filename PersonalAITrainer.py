import cv2, time
import mediapipe as mp
import numpy as np
import PoseEstModule as pem


cap = cv2.VideoCapture('Videos/1.mp4')
ptime = 0
mpDraw = mp.solutions.drawing_utils
detector = pem.PoseEstimation()

direction = 0
count = 0

while True:
    success, img = cap.read()

    if success:
        img = detector.FindPose(img, draw=False)
        lmlist = detector.FindPosition(img, False)
        if len(lmlist) != 0:
            # angle = detector.FindAngle(img, lmlist, 12, 14, 16)   # Right Arm
            angle = detector.FindAngle(img, lmlist, 11, 13, 15, draw=False)    # Left Arm

            per = int(np.interp(angle, [220, 280], [0, 100]))

            # Check for the dumbbell curls
            if per == 100:
                if direction == 0:
                    count += 0.5
                    direction = 1
            if per == 0:
                if direction == 1:
                    count += 0.5
                    direction = 0
                    
            cv2.putText(img, str(int(count)), (200, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)

            
        ctime = time.time()
        fps = 1/ (ctime-ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow('Video', img)
        if cv2.waitKey(10) and  0xFF == ord('q'):
            break
    else:
        break