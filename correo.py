import smtplib
from email.message import EmailMessage


def alertas(subject, body, to):

    msg = EmailMessage()
    msg.set_content(body)

    # Informacion correo
    user = 'pepemon060498@gmail.com'
    password = 'ygsbdetzdblswddy'
    msg['Subject'] = subject
    msg['From'] = "pepemon060498@gmail.com"
    msg['To'] = to

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(user, password)
    s.send_message(msg)
    s.quit()
