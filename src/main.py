import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from cuerpoMail import cuerpo_correo


load_dotenv("dev.env")

# Configuración del correo
from_email = 'ypolanco@dgii.gov.do'
to_email = 'ypolanco@dgii.gov.do'
subject = f'RE: Resumen Avance General Pruebas  | {os.getenv("EQUIPO")}'
html_content = cuerpo_correo

# Configuración del servidor SMTP
smtp_server = "mail.dgii.gov.do"  # Cambia esto al servidor SMTP interno

# Crear el mensaje MIME
message = MIMEMultipart("alternative")
message["Subject"] = subject
message["From"] = from_email
message["To"] = to_email
message.attach(MIMEText(html_content, "html"))

try:
    with smtplib.SMTP(smtp_server) as server:
        # Para ver detalles de la sesión SMTP
        #server.set_debuglevel(1)  # Esto habilita la depuración del servidor
        server.sendmail(from_email, to_email, message.as_string())
        print("Correo enviado exitosamente.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")
