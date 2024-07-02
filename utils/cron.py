from authenticate.models import User, Alerts
from userstats.views import send_alerts, prepare_alerts
from django.core.cache import cache

class CronJob:
    @staticmethod
    def get_users(slot):
     key = "users" + slot
     subscribed_users = cache.get(key)
    
     timeslot=23*60*60
     if subscribed_users is None:
        if slot is "week":
         subscribed_users = User.objects.filter(alerts__weekly=True)
         timeslot=timeslot*7
        
        elif slot is "month":
         subscribed_users = User.objects.filter(alerts__monthly=True)
         timeslot=timeslot*30
        elif slot is "year":
         subscribed_users = User.objects.filter(alerts__yearly=True)
         timeslot=timeslot*365
         
        else:
         subscribed_users = []

     cache.set(key,subscribed_users,timeout=timeslot)
     return subscribed_users
    @staticmethod
    def weekly_alerts():
        subscribed_users = CronJob.get_users()
        for user in subscribed_users.in_bulk(batch_size=100):
            prepare_alerts(user, "week")

    @staticmethod
    def monthly_alerts():
        subscribed_users = User.objects.filter(alerts__monthly=True)
        for user in subscribed_users.in_bulk(batch_size=100):
            prepare_alerts(user, "month")

    @staticmethod
    def year_alerts():
        subscribed_users = User.objects.filter(alerts__yearly=True)
        for user in subscribed_users.in_bulk(batch_size=100):
            prepare_alerts(user, "year")
