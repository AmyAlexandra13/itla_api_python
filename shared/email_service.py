import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailService:
    def __init__(self,
                 smtp_server: str = "smtp.gmail.com",
                 smtp_port: int = 587,
                 email_user: str = "",
                 email_password: str = ""):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_user = email_user
        self.email_password = email_password

    def enviar_email_registro_estudiante(self,
                                         destinatario: str,
                                         nombres: str,
                                         apellidos: str) -> bool:

        try:
            # Crear mensaje
            mensaje = MIMEMultipart()
            mensaje['From'] = self.email_user
            mensaje['To'] = destinatario
            mensaje['Subject'] = "Registro Exitoso - ITLA Sistema Académico"

            # Cuerpo del mensaje
            cuerpo_html = f"""
            <html>
                <body>
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2 style="color: #2E86AB;">¡Bienvenido/a al Sistema Académico ITLA!</h2>

                        <p>Estimado/a <strong>{nombres} {apellidos}</strong>,</p>

                        <p>Nos complace informarte que tu registro en nuestro sistema académico ha sido completado exitosamente.</p>

                        <div style="background-color: #f8f9fa; padding: 20px; border-left: 4px solid #2E86AB; margin: 20px 0;">
                            <h3 style="color: #2E86AB; margin-top: 0;">Próximos pasos:</h3>
                            <ol>
                                <li><strong>Entrega de documentos:</strong> Debes dirigirte a las oficinas de admisión para entregar los siguientes documentos físicos:
                                    <ul>
                                        <li>Cédula de identidad (original y copia)</li>
                                        <li>Acta de nacimiento (original y copia)</li>
                                        <li>Record de bachillerato (original y copia)</li>
                                    </ul>
                                </li>
                                <li><strong>Horario de atención:</strong> Lunes a Viernes de 8:00 AM a 5:00 PM</li>
                                <li><strong>Ubicación:</strong> Oficina de Admisiones, Planta Baja</li>
                            </ol>
                        </div>

                        <div style="background-color: #fff3cd; padding: 15px; border: 1px solid #ffeaa7; border-radius: 5px;">
                            <p style="margin: 0; color: #856404;">
                                <strong>Importante:</strong> Tu solicitud estará en estado "REGISTRADO" hasta que entregues todos los documentos requeridos. Una vez revisados, recibirás una notificación sobre el estado de tu admisión.
                            </p>
                        </div>

                        <p>Si tienes alguna pregunta, no dudes en contactarnos:</p>
                        <ul>
                            <li>Teléfono: (809) 555-0123</li>
                            <li>Email: admisiones@itla.edu.do</li>
                        </ul>

                        <p>¡Esperamos verte pronto en nuestro campus!</p>

                        <p style="margin-top: 30px;">
                            Saludos cordiales,<br>
                            <strong>Equipo de Admisiones ITLA</strong>
                        </p>
                    </div>
                </body>
            </html>
            """

            mensaje.attach(MIMEText(cuerpo_html, 'html'))

            # Enviar email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(mensaje)

            return True

        except Exception as e:
            logging.error(f"Error al enviar email de registro a {destinatario}: {str(e)}")
            return False

email_service = EmailService(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    email_user="thingsrandom950@gmail.com",  # Configurar con tu email
    email_password="xedz vpeo svxm sqjw"   # Configurar con tu contraseña de aplicación
)