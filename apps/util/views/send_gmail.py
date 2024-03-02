import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPAuthenticationError


def sendMail(toaddr, subject, body):
    try:
        fromaddr = "tramite.dirislimasur2021@gmail.com"

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "mikipzxmihguzqvl")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    except SMTPAuthenticationError:
        print("Error al autenticarse")
