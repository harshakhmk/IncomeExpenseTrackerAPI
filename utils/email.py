from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(email_data):
        email = EmailMessage(
            subject=email_data["subject"],
            body=email_data["body"],
            to=[email_data["to_email"]],
        )
        email.send()
