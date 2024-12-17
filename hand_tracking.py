"""
Hand Tracking Module
--------------------
This module uses MediaPipe to detect hands, find landmark positions, determine finger states,
and measure distances between hand landmarks. It is designed to work with OpenCV.

Features:
- Hand detection and drawing hand landmarks.
- Finger position detection.
- Checking which fingers are up.
- Measuring distance between two landmarks.
"""

import cv2
import mediapipe as mp
import time
import math
import numpy as np


class HandDetector:
    """
    A class to detect hands, find landmarks, check finger states, and measure distances.
    """

    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        """
        Initializes the Hand Detector with MediaPipe's hand solution.

        Parameters:
        - mode (bool): Static image mode or not.
        - maxHands (int): Maximum number of hands to detect.
        - modelC (int): Complexity of the detection model.
        - detectionCon (float): Minimum detection confidence.
        - trackCon (float): Minimum tracking confidence.
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelC = modelC

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]  # Landmark IDs for fingertips

        self.lmList = []  # List to store hand landmarks

    def findHands(self, img, draw=True):
        """
        Detects hands in an image and optionally draws landmarks.

        Parameters:
        - img (numpy.ndarray): The input image (BGR format).
        - draw (bool): Whether to draw hand landmarks.

        Returns:
        - img (numpy.ndarray): The output image with landmarks drawn (if enabled).
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for MediaPipe
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        """
        Finds the positions of landmarks for a specified hand.

        Parameters:
        - img (numpy.ndarray): The input image.
        - handNo (int): Index of the hand to analyze.
        - draw (bool): Whether to draw circles at landmark positions.

        Returns:
        - lmList (list): List of [id, x, y] for each landmark.
        - bbox (tuple): Bounding box around the hand (xmin, ymin, xmax, ymax).
        """
        xList, yList = [], []
        bbox = []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self):
        """
        Checks which fingers are up based on landmark positions.

        Returns:
        - fingers (list): A list of 1s (up) or 0s (down) for each finger.
        """
        fingers = []

        # Thumb: Compare x-coordinates
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Four Fingers: Compare y-coordinates
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        """
        Calculates the distance between two landmarks.

        Parameters:
        - p1, p2 (int): Landmark IDs to measure distance.
        - img (numpy.ndarray): The input image.
        - draw (bool): Whether to draw the distance line and circles.
        - r (int): Radius of the circles.
        - t (int): Thickness of the line.

        Returns:
        - length (float): The calculated distance.
        - img (numpy.ndarray): The output image with visualizations (if enabled).
        - lineInfo (list): Coordinates of the two points and the center.
        """
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]


# -------------------- Test the Module --------------------
def main():
    """Test function to display hand landmarks and FPS."""
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    previous_time = 0

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        if len(lmList) != 0:
            print(lmList[4])  # Example: Print position of landmark 4 (thumb tip)

        # Calculate and display FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        # Show the image
        cv2.imshow("Hand Tracking Test", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
