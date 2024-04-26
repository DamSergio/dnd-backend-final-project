import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import CONFIG
from app.utils.jwt import access_security
from app.models.user import User


async def send_email(user: User):
    # TODO: generate a random token
    token = access_security.create_access_token(user.jwt_subject)
    mail_to = user.email
    body = f"""Esto es un email automático.
    
    Para verificar su usuario acceda al siguiente enlace: http://localhost:5173/auth/verify/{token}
    """

    message = MIMEMultipart()
    message["From"] = CONFIG.email_from
    message["To"] = mail_to
    message["Subject"] = "Verificación de usuario"

    message.attach(MIMEText(body, "plain"))

    session = smtplib.SMTP(CONFIG.email_host, CONFIG.email_port)
    session.starttls()

    session.login(CONFIG.email_from, CONFIG.email_password)

    text = message.as_string()

    session.sendmail(CONFIG.email_from, mail_to, text)

    session.quit()
    print(f"Correo enviado a {mail_to}")
