import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
from dotenv import load_dotenv


def send_email(recipient_email, file_path, subject="Your Document", body="Please find your document attached."):
    """
    Send any file as an email attachment using Gmail SMTP
    
    Parameters:
    - recipient_email (str): Email address of the recipient
    - file_path (str): Path to the file to be sent
    - subject (str): Email subject line (optional)
    - body (str): Email body text (optional)
    
    Returns:
    - bool: True if email sent successfully, False otherwise
    """
    load_dotenv()
    sender_email = os.getenv('EMAIL_ADDRESS')
    sender_password = os.getenv('EMAIL_PASSWORD')
    
    if not all([sender_email, sender_password]):
        print("Error: Email credentials not found in .env file")
        return False
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return False
    try:
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(file_path)}'
        )
        msg.attach(part)
    except Exception as e:
        print(f"Error preparing attachment: {e}")
        return False
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    