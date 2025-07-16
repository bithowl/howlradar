import os
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    user = os.getenv("EMAIL_USER")
    pwd = os.getenv("EMAIL_PASS")
    to = os.getenv("EMAIL_TO")
    server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", 587))

    if not all([user, pwd, to]):
        print("Email credentials not set")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = to

    try:
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.login(user, pwd)
        smtp.sendmail(user, [to], msg.as_string())
        smtp.quit()
    except Exception as e:
        print("Email send error:", e)
