# **AI Virtual Mouse Project**

## **Overview**
The **AI Virtual Mouse Project** allows you to control your computer's mouse using hand gestures captured through a webcam. It uses **MediaPipe** for hand tracking, **OpenCV** for image processing, and **pyautogui** for controlling the mouse.

The project is modular, with a hand tracking module for reusability and a main script to implement virtual mouse functionality.

---

## **Features**
- **Cursor Control**: Move the mouse cursor using your index finger.
- **Left Click**: Perform a left-click action by pinching the index and middle fingers.
- **Smooth Movement**: Cursor movement is smoothed to prevent jitter.
- **Virtual Boundary**: Limits movement within a virtual screen boundary.
- **Real-Time FPS Display**: Monitor the frame rate of the webcam feed.

---

## **Project Structure**

```plaintext
AI-Virtual-Mouse/
│
├── virtual_mouse.py       # Main script to run the AI Virtual Mouse
├── hand_tracking.py       # Hand tracking module (MediaPipe + OpenCV)
├── requirements.txt       # Required libraries
└── README.md              # Project documentation
```

---

## **Setup Instructions**

### 1. **Clone the Repository**
Clone this project to your local machine using:

```bash
git clone https://github.com/yourusername/AI-Virtual-Mouse.git
cd AI-Virtual-Mouse
```

### 2. **Install Dependencies**
Install the required libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- OpenCV
- MediaPipe
- pyautogui
- numpy

---

## **How to Run**

1. Ensure your webcam is connected.
2. Run the **`virtual_mouse.py`** script:

```bash
python virtual_mouse.py
```

3. **Controls**:
   - **Move Cursor**: Raise your **index finger** (all other fingers down) to control the cursor.
   - **Left Click**: Pinch your **index finger** and **middle finger** together.
   - **Exit**: Press **`q`** to quit the program.

---

## **File Explanations**

### **1. `virtual_mouse.py`**
This is the main script that:
- Captures video frames from the webcam.
- Detects hands and finger positions using the `hand_tracking` module.
- Controls the mouse cursor and performs clicks using **pyautogui**.

### **2. `hand_tracking.py`**
A utility module for hand detection and tracking:
- Uses MediaPipe to detect hands and their landmarks.
- Provides functions to:
   - Detect which fingers are up.
   - Measure distances between finger landmarks.
   - Find hand positions and bounding boxes.

---

## **Troubleshooting**

1. **Webcam Not Detected**:
   - Ensure the webcam is connected and not used by another program.

2. **Slow Performance**:
   - Reduce webcam resolution in `virtual_mouse.py`:
     ```python
     WEBCAM_WIDTH, WEBCAM_HEIGHT = 320, 240
     ```

3. **Cursor Misalignment**:
   - Adjust the **`FRAME_MARGIN`** and smoothening factor in `virtual_mouse.py` for your screen.

---

## **Future Improvements**
- Add support for right-click and scrolling gestures.
- Introduce gesture-based application switching.
- Optimize performance for lower-end machines.

---# AI-Virtual-Mouse
# AI-Virtual-Mouse
# AI-Virtual-Mouse
# AI-Virtual-Mouse
# AI-Virtual-Mouse
