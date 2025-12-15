# import smtplib
# from email.message import EmailMessage
# import os
# from dotenv import load_dotenv

# load_dotenv()


# def send_email(to_email: str, subject: str, body: str):
#     sender = os.getenv("EMAIL_ADDRESS")
#     password = os.getenv("EMAIL_PASSWORD")
#     print("📧 Sending email from", sender, "to", to_email)


#     if not sender or not password:
#         raise RuntimeError("Email credentials not set")

#     msg = EmailMessage()
#     msg["From"] = sender
#     msg["To"] = to_email
#     msg["Subject"] = subject
#     msg.set_content(body)

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#         server.login(sender, password)
#         server.send_message(msg)

import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()


def send_email(to_email: str, subject: str, body: str):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    print("📧 send_email() CALLED")
    print("📧 From:", sender)
    print("📧 To:", to_email)

    if not sender or not password:
        raise RuntimeError("Email credentials not set")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
            print("✅ EMAIL SENT SUCCESSFULLY")
    except Exception as e:
        print("❌ EMAIL ERROR:", e)
        raise
