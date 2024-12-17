import cv2
import time
import numpy as np
import pyautogui
import hand_tracking as htm

# -------------------- Constants --------------------
WEBCAM_WIDTH, WEBCAM_HEIGHT = 640, 480  # Webcam frame dimensions
FRAME_MARGIN = 100  # Margin to define the virtual screen boundary
SMOOTHENING = 7  # Smoothing factor for mouse movement

# Initialize previous time for FPS calculation
previous_time = 0

# -------------------- Initialize Modules --------------------
# Capture webcam input
cap = cv2.VideoCapture(0)
cap.set(3, WEBCAM_WIDTH)  # Set width
cap.set(4, WEBCAM_HEIGHT)  # Set height

# Check if webcam opens successfully
if not cap.isOpened():
    raise Exception("Error: Webcam not found. Please ensure the webcam is connected.")

# Hand Detector
detector = htm.HandDetector(maxHands=1)

# Screen Size
screen_width, screen_height = pyautogui.size()

# Initialize previous mouse positions for smooth movement
previous_x, previous_y = 0, 0
current_x, current_y = 0, 0


# -------------------- Helper Functions --------------------
def move_mouse_smoothly(x1, y1):
    """
    Smoothly moves the mouse cursor based on the detected finger position.
    """
    global previous_x, previous_y, current_x, current_y

    # Map hand positions to screen dimensions
    mapped_x = np.interp(x1, (FRAME_MARGIN, WEBCAM_WIDTH - FRAME_MARGIN), (0, screen_width))
    mapped_y = np.interp(y1, (FRAME_MARGIN, WEBCAM_HEIGHT - FRAME_MARGIN), (0, screen_height))

    # Smoothening mouse movement
    current_x = previous_x + (mapped_x - previous_x) / SMOOTHENING
    current_y = previous_y + (mapped_y - previous_y) / SMOOTHENING

    # Move the mouse cursor (flip x-axis for alignment)
    pyautogui.moveTo(screen_width - current_x, current_y)

    previous_x, previous_y = current_x, current_y


def perform_left_click(img, length, line_info):
    """
    Performs a left mouse click when two fingers are close together.
    """
    if length < 25:  # If the distance between index and middle fingertips is small
        pyautogui.leftClick()
        cv2.circle(img, (line_info[4], line_info[5]), 15, (0, 255, 0), cv2.FILLED)
        time.sleep(0.3)  # Prevent multiple clicks



def draw_virtual_screen(img):
    """
    Draws a virtual screen boundary rectangle.
    """
    cv2.rectangle(img, (FRAME_MARGIN, FRAME_MARGIN),
                  (WEBCAM_WIDTH - FRAME_MARGIN, WEBCAM_HEIGHT - FRAME_MARGIN),
                  (255, 0, 255), 2)


# -------------------- Main Loop --------------------
def main():
    """
    Main function to run the virtual mouse control using hand gestures.
    """
    global previous_time

    while True:
        # Capture frame-by-frame
        success, img = cap.read()
        if not success:
            print("Error: Could not read frame from webcam.")
            break

        # Detect hands and find positions
        img = detector.findHands(img)
        lm_list, bbox = detector.findPosition(img)

        if len(lm_list) != 0:
            # Get fingertip positions for index and middle fingers
            x1, y1 = lm_list[8][1:]  # Index finger tip
            x2, y2 = lm_list[12][1:]  # Middle finger tip

            # Draw virtual screen boundary
            draw_virtual_screen(img)

            # Check which fingers are up
            fingers = detector.fingersUp()

            # Mouse Movement: Index finger up
            if fingers[1] == 1 and fingers[2] == 0:
                move_mouse_smoothly(x1, y1)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            # Left Click: Index and middle fingers close together
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, line_info = detector.findDistance(8, 12, img)
                perform_left_click(img, length, line_info)


        # Calculate and display FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        cv2.putText(img, f"FPS: {int(fps)}", (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Show the processed frame
        cv2.imshow("AI Virtual Mouse", img)

        # Quit the program on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting AI Virtual Mouse...")
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
