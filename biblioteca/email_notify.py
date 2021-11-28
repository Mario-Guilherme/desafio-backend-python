import smtplib
import ssl


class SendEmail:
    def __init__(self, port=465, receiver_email=None) -> None:

        self.__sender_email = "auxilioestudantilnotificador@gmail.com"
        self.__password = "Shr@46/*+as/ASasj_*$%1"
        self.__server_email = "smtp.gmail.com"
        self.__receiver_email = receiver_email
        self.__context = ssl.create_default_context()
        self.__server = smtplib.SMTP_SSL(
            self.__server_email, port, context=self.__context
        )

    def __login(self):
        return self.__server.login(self.__sender_email, self.__password)
