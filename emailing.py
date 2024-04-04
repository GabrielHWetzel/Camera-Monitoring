import os
from glob import glob
import smtplib
from email.message import EmailMessage
import imghdr
from datetime import datetime

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def send_email(image):
    print("send_email started")
    now = datetime.now().strftime("%H:%M:%S")

    # Email contents
    email_message = EmailMessage()
    email_message["Subject"] = "Camera 0 Alert"
    email_message.set_content(f"Camera 0 detected this object at {now}")
    with open(image, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    # Gmail server
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL, PASSWORD)

    # Send email
    gmail.sendmail(EMAIL, EMAIL, email_message.as_string())

    gmail.quit()
    print("send_email ended")