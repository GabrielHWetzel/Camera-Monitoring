import time
from emailing import send_email

import cv2

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
while True:
    status = 0

    # Video input
    check, frame = video.read()

    # Prepare processing frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Shows camera

    # Capture base static image
    if first_frame is None:
        first_frame = gray_frame_gau

    # Process frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 45, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if rectangle.any():
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list == [1, 0]:
        send_email(frame)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    # Quit key
    if key == ord("q"):
        break

video.release()
