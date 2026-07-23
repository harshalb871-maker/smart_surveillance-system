import datetime
import cv2
import os
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ModuleNotFoundError:
    print("WARNING: python-dotenv is not installed. .env file will not be loaded automatically.")
    print("Install it with: pip install python-dotenv")

class AlertSystem:
    def __init__(self,
                 email_sender=None,
                 email_password=None,
                 alert_recipient=None):
        self.email_sender = email_sender or os.getenv("EMAIL_SENDER")
        self.email_password = email_password or os.getenv("EMAIL_PASSWORD")
        self.alert_recipient = alert_recipient or os.getenv("ALERT_RECIPIENT")

        if not self.email_sender or not self.email_password or not self.alert_recipient:
            print("WARNING: Email/mobile alert configuration is incomplete.")
            print("Set EMAIL_SENDER, EMAIL_PASSWORD, and ALERT_RECIPIENT in the .env file.")

        screenshot_dir = PROJECT_ROOT / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_dir = screenshot_dir

    def trigger_alert(self, alert_type, frame=None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        message = f"[{timestamp}] ALERT: {alert_type} detected!"

        print("\n" + "!" * 50)
        print(message)
        print("!" * 50 + "\n")

        if frame is not None:
            filename = self.screenshot_dir / f"alert_{timestamp}.jpg"
            cv2.imwrite(str(filename), frame)
            print(f"--> Screenshot saved to {filename}")

        if self.email_sender and self.email_password and self.alert_recipient:
            msg = MIMEText(message)
            msg["Subject"] = "Smart Surveillance Alert"
            msg["From"] = self.email_sender
            msg["To"] = self.alert_recipient

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(self.email_sender, self.email_password)
                    server.sendmail(self.email_sender, self.alert_recipient, msg.as_string())
                print("--> Alert sent to mobile/email recipient.")
            except Exception as e:
                print(f"--> Failed to send alert email: {e}")
        else:
            print("--> Email/mobile alert not sent because credentials or recipient are missing.")
        
