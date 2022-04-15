from cgitb import html
from email import message
from email.generator import DecodedGenerator
from email.mime import base
import os
from loguru import logger
from matplotlib.pyplot import text
from pathlib import Path
import base64

MAX_FILE_SIZE = 2000000
SENDER_EMAIL = "christesting789@gmail.com"
RECEIVER_EMAIL = ["christesting160@gmail.com","christesting124@gmail.com"]
CC_EMAIL = ""

def password():
    MY_PASSWORD = "Chris1996!".encode('utf-8')
    base64_bytes = base64.b64encode(MY_PASSWORD)
    decoded_bytes = base64.b64decode(base64_bytes)
    pwd1 = decoded_bytes.decode()
    return pwd1


def send_alert(subject, body, files): #, files
    import smtplib
    from smtplib import SMTPException
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email import encoders

    sender_email = SENDER_EMAIL

    receiver_email = RECEIVER_EMAIL
    cc_emails =  CC_EMAIL
    
    #to_emails = receiver_email.split(',') 

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(receiver_email)          # receiver_email
    message['Subject'] = subject 
    message['CC'] = cc_emails

    message.attach(MIMEText(body, 'html'))

    for filename in files:
        attach_path = filename
        if attach_path.exists() and os.path.getsize(filename) < MAX_FILE_SIZE:
            with open(os.path.join(filename), 'rb') as attachment:
                part = MIMEBase('application', 'octect-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename = {os.path.basename(filename)}",)
            message.attach(part)
        else:
            att = attach_path.as_posix()
            logger.warning(f"Failed to attach {att} as the path did not exist or the file was larger than {MAX_FILE_SIZE} bytes.")

    text = message.as_string()
    
    try:
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587) # Google port number
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        
        smtpobj.login(sender_email, password())
        smtpobj.sendmail(sender_email, receiver_email, text)
        smtpobj.close()
    except SMTPException:
        logger.exception(f"Unable to send email. Failed to send from {sender_email} to {','.join(receiver_email)}.")