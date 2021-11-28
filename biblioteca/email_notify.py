import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class SendEmail:
    def __init__(
        self, port=465, path_file: str = None, receiver_email: str = None
    ) -> None:

        self.__sender_email = "auxilioestudantilnotificador@gmail.com"
        self.__password = "Shr@46/*+as/ASasj_*$%1"
        self.__server_email = "smtp.gmail.com"
        self.__receiver_email = receiver_email
        self.__context = ssl.create_default_context()
        self.__server = smtplib.SMTP_SSL(
            self.__server_email, port, context=self.__context
        )
        self.__path_file = path_file

    def create_mail_to_send(self) -> MIMEMultipart:
        message = MIMEMultipart()
        message["From"] = self.__sender_email
        message["To"] = self.__receiver_email
        message["Subject"] = "Dados do banco de dados"
        body = "\nDados"
        message.attach(MIMEText(body, "plain"))
        return message

    def convert_file_base64(self):
        attachment = open(self.__path_file, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", "attachment; filename= %s" % self.__path_file
        )
        message = self.create_mail_to_send()
        message.attach(part)
        attachment.close()

    def __login(self):
        return self.__server.login(self.__sender_email, self.__password)
