import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText


class EMailBackend:
    def __init__(self, username, passwd, server_name, sender_email):
        self.server = smtplib.SMTP(server_name, 587)
        self.server.starttls()
        self.server.login(username, passwd)
        self.sender = sender_email

    def send(self, receivers, subject, body, attachments, cc, bcc):
        all_receivers = receivers + cc + bcc

        message = MIMEMultipart()
        message["From"] = self.sender
        message["To"] = ",".join(receivers)
        message["Cc"] = ",".join(cc)
        message["Subject"] = subject
        message.add_header('reply-to', self.sender)
        message.attach(MIMEText(body, "html"))

        for filename, attachment in attachments:
            part = MIMEBase('application', "octet-stream")
            temp = attachment.read()
            part.set_payload(temp)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(filename))
            message.attach(part)

        self.server.sendmail(self.sender,
                             all_receivers,
                             message.as_string())

    def close(self):
        self.server.quit()
