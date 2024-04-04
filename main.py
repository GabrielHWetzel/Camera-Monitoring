import time
from emailing import send_email
import cv2
from glob import glob
import os

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
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob("images/*.png")

    # Check if object left the image
    status_list.append(status)
    status_list = status_list[-2:]

    # Send email on exit image
    if status_list == [1, 0]:
        print(send_email(frame))
        for image in glob("images/*.png"):
            os.remove(image)
    # Shows camera
    cv2.imshow("Camera", frame)
    # Quit key
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
video.release()
