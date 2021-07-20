from notifications.signals import notify


class Notifications:
    @staticmethod
    def send_notification(sender, recipient, message):
        try:
            notify.send(
                actor=sender, recipient=recipient, verb="Message", description=message
            )
        except Exception as e:
            pass
