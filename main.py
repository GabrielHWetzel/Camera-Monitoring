import os
from glob import glob
import time
import cv2
from emailing import send_email
from threading import Thread


def clean_folder():
    print("clean_folder started")
    for image in glob("frames/*.png"):
        os.remove(image)
    print("clean_folder ended")


video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

while True:
    status = 0
    # Video input
    check, frame = video.read()

    # Process frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    # Capture base static image
    if first_frame is None:
        first_frame = gray_frame_gau
    # Process frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 45, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Draw rectangle around object
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if rectangle.any():
            status = 1
            # Save Image
            cv2.imwrite(f"frames/{count}.png", frame)
            count = count + 1
            all_frames = glob("frames/*.png")
            index = int(len(all_frames)/2)
            target_frame = all_frames[index]

    # Check if object left the image
    status_list.append(status)
    status_list = status_list[-2:]
    # Send email on exit image
    if status_list == [1, 0]:
        # Prepare thread
        print(target_frame)
        email_thread = Thread(target=send_email, args=(target_frame, ))
        email_thread.daemon = True
        email_thread.start()

    # Shows camera
    cv2.imshow("Camera", frame)
    # Quit key
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
video.release()
clean_folder()
