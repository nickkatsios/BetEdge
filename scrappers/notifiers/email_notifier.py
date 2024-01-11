from notifiers.notifier_interface import Notifier_interface
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from os.path import join, dirname
import logging

class Email_notifier(Notifier_interface):
    """
    Email notifier class

    Sends an email to the specified receiver

    Attributes:
        sender: The email address of the sender
        receiver: The email address of the receiver
        GMAIL_CRED: The secret key of the sender's gmail address
        (Obtain one from https://myaccount.google.com/apppasswords)
    """

    def __init__(self, sender, receiver):
        dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '.env')
        load_dotenv(dotenv_path)
        self.sender = sender
        self.receiver = receiver
        self.GMAIL_CRED = os.getenv('GMAIL_CRED')

    def notify_error(self, error_message):
        """Sends an error email to the specified receiver
        
        Args:
            error_message: The message to be sent
        """
        try: 
            root_logger = logging.getLogger()
            
            mail = EmailMessage()
            mail["Subject"] = "Error from BetEdge Scrappers"
            mail["From"] =  self.sender
            mail["To"] = self.receiver
            mail.set_content(error_message)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.sender, self.GMAIL_CRED)
                smtp.send_message(mail)
                root_logger.info("--------------- Error Email sent successfully ---------------")
        except Exception as e:
            print("Error sending email: " + str(e))
            pass