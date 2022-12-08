import helper
from da_bell_secrets import *
from providers import PROVIDERS
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pathlib

''' 
This program sends an SMS/MMS message to the 
owner of a Da Bell device to notify them that 
the doorbell was pressed along with a photo. 

Info: Attachment can be at most 1MB
Had to learn that the hard way.
'''

def send_text_message(file_path):
    __send_mms_via_email(file_path)

@helper.threaded
def __send_mms_via_email(file_path):
    # initialize variables needed
    phone_number: str = PHONE_NUMBER
    door_ring_message: str = helper.DOOR_RING_MESSAGE
    file_path: str = file_path
    mime_maintype: str = helper.FILE_TYPE
    mime_subtype: str = pathlib.Path(file_path).suffix
    file_name: str = pathlib.Path(file_path).name
    phone_provider: str = PHONE_PROVIDER
    sender_credentials: tuple = SENDER_CREDENTIALS
    subject: str = helper.APP_NAME
    smtp_server: str = helper.SMTP_GMAIL
    smtp_port: int = helper.SMTP_PORT
    
    # get/create information needed to send message
    # get gmail and password from da_bell_secrets.py
    sender_email, email_password = sender_credentials
    
    # get message type (sms/mms) based on provider
    # some do not allow mms
    message_type = helper.MESSAGE_TYPE[0] \
        if PROVIDERS.get(phone_provider).get(helper.MMS_SUPPORT_KEY) \
        else helper.MESSAGE_TYPE[0]
        
    # create receiver email based on their phone number and carrier
    receiver_email = f'{phone_number}@{PROVIDERS.get(phone_provider).get(message_type)}'
    
    # create gmail body
    email_message = MIMEMultipart()
    email_message["Subject"] = subject
    email_message["From"] = sender_email
    email_message["To"] = receiver_email
    email_message.attach(MIMEText(door_ring_message, helper.TEXT_TYPE))
    
    # open file being sent and attach to email_message
    with open(file_path, helper.READ_BINARY) as attachment:
        part = MIMEBase(mime_maintype, mime_subtype)
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename={file_name}",
        )
        email_message.attach(part)

    # send the message
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context = ssl.create_default_context()) as email:
        # securely login to gmail
        email.login(sender_email, email_password)
        # send email with body and attachment
        email.sendmail(sender_email, receiver_email, email_message.as_string())
        print("Da Bell owner notified that doorbell was pressed")
        