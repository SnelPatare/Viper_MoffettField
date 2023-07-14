import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email():
    # Create a multipart message object
    # Example usage
    sender_email = 'demoviper321@gmail.com'
    sender_password = 'acauhrlrmextqxzd'
    recipient_email = 'demoviper321@gmail.com'
    subject = 'Moffet Field Museum'
    message = 'Thank you for visiting Moffet Feild Historical Museum'
    attachment_path = './Photos/savedImage.jpg'
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Create HTML part of the message
    html_message = MIMEText(message, 'html')
    msg.attach(html_message)

    # Open the file in bytemode and attach it as a MIMEBase object
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Encode the file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add headers to the attachment and attach it to the email
    part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
    msg.attach(part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())



send_email()

