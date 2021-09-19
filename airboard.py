import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from datetime import datetime
import numpy as np
import os
import subprocess
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    pyautogui.PAUSE = 0
    MAX_NUM_HANDS = 1
    pyautogui.FAILSAFE = False


    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands


    screen_width, screen_height = pyautogui.size()


    index_knuckle_location_storage_x = np.zeros([5]) 
    index_knuckle_location_storage_y = np.zeros([5])

    wrist_location_storage_x = np.zeros([5]) 
    wrist_location_storage_y = np.zeros([5]) 

    index_location_storage_x = np.zeros([5]) 
    index_location_storage_y = np.zeros([5]) 

    buffer = 0
    bufferStart = -11

    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                image_height, image_width, _ = image.shape
                image_depth = -1
                for hand_landmarks in results.multi_hand_landmarks:


                    # getting the location of the index, index knuckle, wrist, pinky, and thumb in terms of screen pixels
                    x_location_index_knuckle = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * screen_width * 1.5 - 0.2 * screen_width
                    y_location_index_knuckle = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * screen_height * 1.5 - 0.2 * screen_height

                    x_location_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * screen_width * 1.5 - 0.2 * screen_width
                    y_location_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * screen_height * 1.5 - 0.2 * screen_height

                    x_location_wrist = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x * screen_width * 1.5 - 0.2 * screen_width
                    y_location_wrist = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * screen_height * 1.5 - 0.2 * screen_height

                    thumb_location_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * screen_width * 1.5 - 0.2 * screen_width
                    thumb_location_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * screen_height * 1.5 - 0.2 * screen_height

                    pinky_location_x = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * screen_width * 1.5 - 0.2 * screen_width
                    pinky_location_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * screen_height * 1.5 - 0.2 * screen_height

                    middle_location_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * screen_width * 1.5 - 0.2 * screen_width
                    middle_location_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * screen_height * 1.5 - 0.2 * screen_height

                    ring_location_x = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * screen_width * 1.5 - 0.2 * screen_width
                    ring_location_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * screen_height * 1.5 - 0.2 * screen_height
            

                    # updating the storage arrays if there is movement in both the wrist and knuckle
                    if((abs(x_location_wrist - wrist_location_storage_x[-1]) > 5) and ((abs(x_location_index_knuckle - index_knuckle_location_storage_x[-1]) > 5))):
                        wrist_location_storage_x = np.roll(wrist_location_storage_x, 1)
                        wrist_location_storage_x[0] = x_location_wrist

                        index_knuckle_location_storage_x = np.roll(index_knuckle_location_storage_x, 1)
                        index_knuckle_location_storage_x[0] = x_location_index_knuckle

                    if((abs(y_location_wrist - wrist_location_storage_y[-1]) > 5) and ((abs(y_location_index_knuckle - index_knuckle_location_storage_y[-1]) > 5))):
                        wrist_location_storage_y = np.roll(wrist_location_storage_y, 1)
                        wrist_location_storage_y[0] = y_location_wrist

                        index_knuckle_location_storage_y = np.roll(index_knuckle_location_storage_y, 1)
                        index_knuckle_location_storage_y[0] = y_location_index_knuckle


                    # have not updated the index array so must do that now
                    index_location_storage_x = np.roll(index_location_storage_x, 1)
                    index_location_storage_x[0] = x_location_index

                    index_location_storage_y = np.roll(index_location_storage_y, 1)
                    index_location_storage_y[0] = y_location_index


                    # find the average of the knuckle for cursor location and the index for clicking
                    mouse_x = np.average(index_knuckle_location_storage_x)
                    mouse_y = np.average(index_knuckle_location_storage_y)

                    index_average_location_x = np.average(index_location_storage_x)
                    index_average_location_y = np.average(index_location_storage_y)

                    
                    # movement
                    pyautogui.moveTo(mouse_x, mouse_y)

                    buffer += 1
                    if buffer > bufferStart + 10:

                        # left click
                        if abs(thumb_location_x - index_average_location_x) < 100:
                            if abs(thumb_location_y - index_average_location_y) < 100:
                                print("click")
                                pyautogui.click(mouse_x, mouse_y, clicks = 1, duration = 0.1, button = 'left')
                                bufferStart = buffer

                        # right click
                        if abs(thumb_location_x - middle_location_x) < 100:
                            if abs(thumb_location_y - middle_location_y) < 100:
                                print("right click")
                                pyautogui.click(mouse_x, mouse_y, clicks = 1, duration = 0.1, button = 'right')
                                bufferStart = buffer

                        # double click
                        if abs(thumb_location_x - pinky_location_x) < 100:
                            if abs(thumb_location_y - pinky_location_y) < 100:
                                print("double click")
                                pyautogui.doubleClick(mouse_x, mouse_y)
                                bufferStart = buffer

                        # bring up keyboard
                        if abs(thumb_location_x - ring_location_x) < 100:
                            if abs(thumb_location_y - ring_location_y) < 100:
                                print("keyboard")
                                pyautogui.hotkey('ctrl', 'win', 'o')
                                bufferStart = buffer

                
                        # calculate swipe change in y direction
                        swipeYValue = index_location_storage_y[-3] - index_location_storage_y[0]

                        # swipe up
                        if(swipeYValue > 300):
                            print("swiped up")
                            pyautogui.scroll(-450)
                            bufferStart = buffer

                        # swipe down
                        elif(swipeYValue < -300):
                            print("swiped down")
                            pyautogui.scroll(450)
                            bufferStart = buffer


                    # end of code
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()

else:
    
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
