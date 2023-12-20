from flask_mail import Mail as flaskMail, Message


class Mail(flaskMail):
    def __init__(self, *args, **kwargs):
        super(Mail, self).__init__(*args, **kwargs)

    def send(self, recipients: list, subject: str = "", body: str = ""):
        msg = Message(
            subject=subject,
            sender=self.app.config['EMAIL'],
            recipients=recipients
        )
        msg.html = body
        super(Mail, self).send(msg)
        return True
