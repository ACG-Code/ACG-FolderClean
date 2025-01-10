import ssl
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.message import EmailMessage
# TODO: Replace this import with one relevant to client

class LogEmailer:
    @staticmethod
    def send_log_emails(tm1_server_name : str, recipients : list, logs : dict):
        current_datetime = datetime.now()

        # TODO: Edit to user and password specific to server
        # Have a secure way to retrieve these values
        # This is an example of an 'app password'
        port = 587
        smtp_server_address = 'smtp.gmail.com'
        sender_email_address = 'vcinardo@gmail.com'
        sender_email_password = 'sbmg kvjo amwd visw'
        context = ssl.create_default_context()
        smtp_server = smtplib.SMTP(smtp_server_address, port=port)
        smtp_server.ehlo()
        smtp_server.starttls(context=context)
        smtp_server.ehlo()

        # TODO: Change login in a way specific to the server
        smtp_server.login(sender_email_address, sender_email_password)

        # Creating the body of the email
        email_message = ''
        for log in logs:
            email_message += f'{log}\n'
        email_body = MIMEText(email_message, 'plain')

        for recipient_email_address in recipients:
            email = EmailMessage()
            email['Subject'] = f'Error logs {tm1_server_name}:{current_datetime}'
            email['From'] = sender_email_address
            email['To'] = recipient_email_address
            email.attach(email_message)
            smtp_server.send_message(email_body)
        smtp_server.quit()