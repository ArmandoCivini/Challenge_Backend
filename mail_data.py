import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVER = "localhost"
PORT = 1025


def send_mail():
    subject = "Countries data and stats"
    body = "attached the excel file with the data and stats of the countries"
    sender_email = "my@gmail.com"
    receiver_email = "your@gmail.com"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "challenge.xlsx"

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    server = smtplib.SMTP(SERVER, PORT)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
