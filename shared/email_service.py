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

    def enviar_email_documentos_completos(self,
                                          destinatario: str,
                                          nombres: str,
                                          apellidos: str) -> bool:
        """
        Envía email al estudiante cuando ha subido todos los documentos requeridos
        """
        try:
            # Crear mensaje
            mensaje = MIMEMultipart()
            mensaje['From'] = self.email_user
            mensaje['To'] = destinatario
            mensaje['Subject'] = "Documentos Recibidos - ITLA Sistema Académico"

            # Cuerpo del mensaje
            cuerpo_html = f"""
              <html>
                  <body>
                      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                          <h2 style="color: #2E86AB;">¡Documentos Recibidos Exitosamente!</h2>

                          <p>Estimado/a <strong>{nombres} {apellidos}</strong>,</p>

                          <p>Nos complace informarte que hemos recibido todos los documentos requeridos para tu proceso de admisión en ITLA.</p>

                          <div style="background-color: #d4edda; padding: 20px; border-left: 4px solid #28a745; margin: 20px 0;">
                              <h3 style="color: #155724; margin-top: 0;">📋 Documentos Recibidos:</h3>
                              <ul style="color: #155724;">
                                  <li>✅ Cédula de Identidad</li>
                                  <li>✅ Acta de Nacimiento</li>
                                  <li>✅ Record de Bachillerato</li>
                              </ul>
                          </div>

                          <div style="background-color: #fff3cd; padding: 15px; border: 1px solid #ffeaa7; border-radius: 5px; margin: 20px 0;">
                              <h4 style="color: #856404; margin-top: 0;">🔍 Proceso de Validación</h4>
                              <p style="margin: 0; color: #856404;">
                                  Nuestro equipo de admisiones está validando todos tus documentos para aprobar tu ingreso a la institución. 
                                  Este proceso puede tomar entre <strong>3 a 5 días hábiles</strong>.
                              </p>
                          </div>

                          <div style="background-color: #f8f9fa; padding: 20px; border-left: 4px solid #2E86AB; margin: 20px 0;">
                              <h4 style="color: #2E86AB; margin-top: 0;">📧 Próximos pasos:</h4>
                              <ul style="color: #495057;">
                                  <li>Recibirás una notificación por correo con el resultado de la validación</li>
                                  <li>Si tus documentos son aprobados, te enviaremos información sobre matrícula</li>
                                  <li>Si hay algún inconveniente, te contactaremos para solicitar documentos adicionales</li>
                              </ul>
                          </div>

                          <div style="text-align: center; margin: 30px 0; padding: 20px; background-color: #e7f3ff; border-radius: 10px;">
                              <h3 style="color: #0066cc; margin-top: 0;">🎉 ¡Gracias por elegir ITLA!</h3>
                              <p style="color: #004499; margin-bottom: 0;">
                                  Estamos emocionados de tenerte como parte de nuestra comunidad académica.
                              </p>
                          </div>

                          <p>Si tienes alguna pregunta durante el proceso, no dudes en contactarnos:</p>
                          <ul>
                              <li>📞 Teléfono: (809) 555-0123</li>
                              <li>📧 Email: admisiones@itla.edu.do</li>
                              <li>🕒 Horario: Lunes a Viernes de 8:00 AM a 5:00 PM</li>
                          </ul>

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
            logging.error(f"Error al enviar email de documentos completos a {destinatario}: {str(e)}")
            return False

    def enviar_email_documentos_validados(self,
                                          destinatario: str,
                                          nombres: str,
                                          apellidos: str) -> bool:

        try:
            mensaje = MIMEMultipart()
            mensaje['From'] = self.email_user
            mensaje['To'] = destinatario
            mensaje['Subject'] = "Documentos Validados - ITLA Sistema Académico"

            cuerpo_html = f"""
              <html>
                  <body>
                      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                          <h2 style="color: #2E86AB;">¡Excelentes Noticias! 🎉</h2>

                          <p>Estimado/a <strong>{nombres} {apellidos}</strong>,</p>

                          <p>Nos complace informarte que todos tus documentos han sido <strong>procesados y validados exitosamente</strong> por nuestro equipo de admisiones.</p>

                          <div style="background-color: #d4edda; padding: 20px; border-left: 4px solid #28a745; margin: 20px 0;">
                              <h3 style="color: #155724; margin-top: 0;">✅ Documentos Validados:</h3>
                              <ul style="color: #155724;">
                                  <li>✅ Cédula de Identidad - <strong>VÁLIDO</strong></li>
                                  <li>✅ Acta de Nacimiento - <strong>VÁLIDO</strong></li>
                                  <li>✅ Record de Bachillerato - <strong>VÁLIDO</strong></li>
                              </ul>
                              <p style="margin-bottom: 0; color: #155724; font-weight: bold;">
                                  🎊 ¡Todos tus documentos cumplen con nuestros requisitos académicos!
                              </p>
                          </div>

                          <div style="background-color: #fff3cd; padding: 20px; border-left: 4px solid #ffc107; margin: 20px 0;">
                              <h3 style="color: #856404; margin-top: 0;">📋 Estado Actual: PENDIENTE DE RESPUESTA</h3>
                              <p style="color: #856404; margin-bottom: 10px;">
                                  Tu solicitud de admisión está ahora en proceso de <strong>evaluación final</strong> por parte del comité académico.
                              </p>
                              <ul style="color: #856404; margin: 10px 0;">
                                  <li><strong>Tiempo estimado de respuesta:</strong> 5 a 7 días hábiles</li>
                                  <li><strong>Próximo paso:</strong> Evaluación académica integral</li>
                                  <li><strong>Decisión final:</strong> Aceptación o solicitud de información adicional</li>
                              </ul>
                          </div>

                          <div style="background-color: #e7f3ff; padding: 20px; border-radius: 10px; margin: 20px 0;">
                              <h3 style="color: #0066cc; margin-top: 0;">🔔 ¿Qué sigue ahora?</h3>
                              <ol style="color: #004499;">
                                  <li><strong>Mantente atento a tu correo:</strong> Te notificaremos inmediatamente cuando tengamos una decisión</li>
                                  <li><strong>Prepárate para el siguiente paso:</strong> Si eres aceptado, recibirás información sobre matrícula</li>
                                  <li><strong>No necesitas hacer nada más:</strong> Tu proceso está completo por tu parte</li>
                              </ol>
                          </div>

                          <div style="text-align: center; margin: 30px 0; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
                              <h3 style="color: #2E86AB; margin-top: 0;">🙏 ¡Gracias por tu paciencia!</h3>
                              <p style="color: #6c757d; margin-bottom: 0;">
                                  Apreciamos el esfuerzo que has puesto en completar tu solicitud. 
                                  <br><strong>¡Estamos emocionados de poder tenerte en nuestra comunidad académica!</strong>
                              </p>
                          </div>

                          <div style="background-color: #f1f3f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                              <h4 style="color: #5f6368; margin-top: 0;">📞 ¿Tienes alguna pregunta?</h4>
                              <p style="color: #5f6368; margin: 5px 0;">
                                  <strong>Teléfono:</strong> (809) 555-0123 <br>
                                  <strong>Email:</strong> admisiones@itla.edu.do <br>
                                  <strong>Horario:</strong> Lunes a Viernes de 8:00 AM a 5:00 PM
                              </p>
                          </div>

                          <p style="margin-top: 30px;">
                              Con admiración y mejores deseos,<br>
                              <strong>Equipo de Admisiones ITLA</strong><br>
                              <em>"Construyendo el futuro tecnológico de República Dominicana"</em>
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
            logging.error(f"Error al enviar email de documentos validados a {destinatario}: {str(e)}")
            return False

    def enviar_email_admision_aceptada(
            self,
            destinatario: str,
            nombres: str,
            apellidos: str,
            matricula: str
    ) -> bool:

        try:
            asunto = "¡Felicitaciones! Tu admisión ha sido aceptada"

            mensaje = MIMEMultipart()
            mensaje['From'] = self.email_user
            mensaje['To'] = destinatario
            mensaje['Subject'] = asunto


            cuerpo_html = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                        .container {{ max-width: 600px; margin: 0 auto; background-color: #f9f9f9; padding: 30px; border-radius: 10px; }}
                        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                        .content {{ background-color: white; padding: 30px; margin: 0; }}
                        .matricula {{ background-color: #e8f5e8; border: 2px solid #4CAF50; padding: 15px; margin: 20px 0; text-align: center; border-radius: 5px; }}
                        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
                        .success {{ color: #4CAF50; font-weight: bold; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>¡Admisión Aceptada!</h1>
                        </div>
                        <div class="content">
                            <p>Estimado/a <strong>{nombres} {apellidos}</strong>,</p>

                            <p class="success">¡Felicitaciones! Nos complace informarte que tu solicitud de admisión ha sido <strong>ACEPTADA</strong>.</p>

                            <p>Te damos la más cordial bienvenida a nuestra institución educativa. Estamos emocionados de tenerte como parte de nuestra comunidad académica.</p>

                            <div class="matricula">
                                <h3>Tu número de matrícula es:</h3>
                                <h2 style="color: #4CAF50; margin: 10px 0;">{matricula}</h2>
                                <p><em>Guarda este número, lo necesitarás para todos tus trámites académicos.</em></p>
                            </div>

                            <p><strong>Próximos pasos:</strong></p>
                            <ul>
                                <li>Conserva tu número de matrícula en un lugar seguro</li>
                                <li>Mantente atento a futuras comunicaciones sobre el proceso de inscripción</li>
                                <li>Si tienes dudas, no dudes en contactarnos</li>
                            </ul>

                            <p>Una vez más, ¡felicitaciones y bienvenido/a!</p>

                            <p>Atentamente,<br>
                            <strong>Equipo de Admisiones</strong></p>
                        </div>
                        <div class="footer">
                            <p>Este es un mensaje automático, por favor no responder a este correo.</p>
                        </div>
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
            logging.error(f"Error al enviar email de admisión aceptada: {str(e)}")
            return False

    def enviar_email_admision_rechazada(
            self,
            destinatario: str,
            nombres: str,
            apellidos: str
    ) -> bool:
        """
        Envía email de notificación cuando la admisión del estudiante es rechazada
        """
        try:
            asunto = "Resultado de tu solicitud de admisión"

            mensaje = MIMEMultipart()
            mensaje['From'] = self.email_user
            mensaje['To'] = destinatario
            mensaje['Subject'] = asunto

            # Crear el contenido HTML del email
            contenido_html = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                        .container {{ max-width: 600px; margin: 0 auto; background-color: #f9f9f9; padding: 30px; border-radius: 10px; }}
                        .header {{ background-color: #f44336; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                        .content {{ background-color: white; padding: 30px; margin: 0; }}
                        .info-box {{ background-color: #fff3cd; border: 2px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>Resultado de Admisión</h1>
                        </div>
                        <div class="content">
                            <p>Estimado/a <strong>{nombres} {apellidos}</strong>,</p>

                            <p>Agradecemos tu interés en formar parte de nuestra institución educativa y el tiempo que dedicaste al proceso de admisión.</p>

                            <p>Lamentamos informarte que, después de una cuidadosa evaluación de tu solicitud y documentación, <strong>no podemos ofrecerte un lugar en esta ocasión</strong>.</p>

                            <div class="info-box">
                                <p><strong>Esta decisión no refleja tu valía personal o académica.</strong> El proceso de admisión es altamente competitivo y debemos tomar decisiones difíciles debido a la limitada disponibilidad de cupos.</p>
                            </div>

                            <p><strong>Te animamos a:</strong></p>
                            <ul>
                                <li>Considerar aplicar nuevamente en el próximo período de admisiones</li>
                                <li>Explorar otras oportunidades educativas que se alineen con tus objetivos</li>
                                <li>Continuar preparándote académicamente para futuras oportunidades</li>
                            </ul>

                            <p>Te deseamos mucho éxito en tus futuros emprendimientos académicos y profesionales.</p>

                            <p>Atentamente,<br>
                            <strong>Equipo de Admisiones</strong></p>
                        </div>
                        <div class="footer">
                            <p>Este es un mensaje automático, por favor no responder a este correo.</p>
                        </div>
                    </div>
                </body>
            </html>
            """

            mensaje.attach(MIMEText(contenido_html, 'html'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(mensaje)

            return True

        except Exception as e:
            logging.error(f"Error al enviar email de admisión rechazada: {str(e)}")
            return False


email_service = EmailService(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    email_user="thingsrandom950@gmail.com",  # Configurar con tu email
    email_password="xedz vpeo svxm sqjw"   # Configurar con tu contraseña de aplicación
)


