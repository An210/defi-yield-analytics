import os
import smtplib
from email.mime.text import MIMEText
import logging

def send_alert(to_email, pool_name, apy_change):
    msg = MIMEText(f"APY change for {pool_name}: {apy_change}%")
    msg["Subject"] = "DeFi Yield Alert"
    msg["From"] = os.getenv("ALERT_EMAIL_FROM", "your@email.com")
    msg["To"] = to_email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(
                os.getenv("ALERT_EMAIL_USER"),
                os.getenv("ALERT_EMAIL_PASS")
            )
            server.send_message(msg)
    except Exception as e:
        logging.error(f"Error sending alert: {e}")
