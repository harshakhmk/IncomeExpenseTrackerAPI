from django.shortcuts import render
from rest_framework.views import APIView
import datetime
from rest_framework import status, response
from expenses.models import *
from rest_framework import permissions
from utils.permission import *
from authenticate.models import Alerts, User
from utils.email import Util
from utils.notifications import Notifications
from utils.sms import send_sms
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from authenticate.models import *

admin_user = User.objects.all().filter(is_superuser=True)
bot_user = User.objects.get(email="botIETeam@gmail.com")

class ExpenseSummaryStats(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    @staticmethod
    def get_category(expense):
        return expense.category

    @staticmethod
    def get_amount_of_category(category, expenses):
        amount = 0
        category_expenses = list(expenses.filter(category=category))
        for ce in category_expenses:
            amount = amount + ce.amount
        return {"amount": str(amount)}

    token_param = openapi.Parameter(
        "timegap",
        in_=openapi.IN_QUERY,
        description="Enter week/month/year to get records",
        type=openapi.TYPE_STRING,
    )

    @staticmethod
    def get_data(user, date):
        today_date = datetime.date.today()
        year_back = today_date - datetime.timedelta(days=12 * 30)
        month_back = today_date - datetime.timedelta(days=30)
        week_back = today_date - datetime.timedelta(days=7)

        expenses = Expense.objects.filter(user=request.user)
        # Transaction from last year
        if date.lower() == "year":
            expenses = expenses.filter(
                transaction_date__gte=year_back, transaction_date__lte=today_date
            )

        # Transaction from last month
        elif date.lower() == "month":
            expenses = expenses.filter(
                transaction_date__gte=month_back, credited_date__lte=today_date
            )

        # Transaction from last week
        elif date.lower() == "week":
            expenses = expenses.filter(
                transaction_date__gte=month_back, transaction_date__lte=today_date
            )

        response_data = {}
        # map returns list of categires of expenses queryset
        categories = list(set(map(ExpenseSummaryStats.get_category, expenses)))

        for category in categories:
            response_data[category] = ExpenseSummaryStats.get_amount_of_category(
                category, expenses
            )
        return response_data

    @swagger_auto_schema(manual_parameters=[token_param])
    def get(self, request):
        date = request.GET.get("timegap", "")
        response_data = ExpenseSummaryStats.get_data(request.user, date)
        return response.Response(
            {"category_expense": response_data}, status=status.HTTP_200_OK
        )


# Income stats


class IncomeSummaryStats(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    @staticmethod
    def get_category(income):
        return income.category

    @staticmethod
    def get_amount_of_category(category, income):
        amount = 0
        category_income = list(income.filter(category=category))
        for ce in category_income:
            amount = amount + ce.amount
        return {"amount": str(amount)}

    token_param = openapi.Parameter(
        "timegap",
        in_=openapi.IN_QUERY,
        description="Enter week/month/year to get records",
        type=openapi.TYPE_STRING,
    )

    @staticmethod
    def get_data(user, date):
        today_date = datetime.date.today()
        year_back = today_date - datetime.timedelta(days=12 * 30)
        month_back = today_date - datetime.timedelta(days=30)
        week_back = today_date - datetime.timedelta(days=7)

        income = Income.objects.filter(user=user)

        # Transaction from last year
        if date.lower() == "year":
            income = income.filter(
                credited_date__gte=year_back, credited_date__lte=today_date
            )

        # Transaction from last month
        elif date.lower() == "month":
            income = income.filter(
                credited_date__gte=month_back, credited_date__lte=today_date
            )

        # Transaction from last week
        elif date.lower() == "week":
            income = income.filter(
                credited_date__gte=month_back, credited_date__lte=today_date
            )

        response_data = {}
        # map returns list of categires of income queryset
        categories = list(set(map(IncomeSummaryStats.get_category, income)))

        for category in categories:
            response_data[category] = IncomeSummaryStats.get_amount_of_category(
                category, income
            )
        return response_data

    @swagger_auto_schema(manual_parameters=[token_param])
    def get(self, request):

        date = request.GET.get("timegap", "")

        response_data = IncomeSummaryStats.get_data(request.user, date)

        return response.Response(
            {"category_expense": response_data}, status=status.HTTP_200_OK
        )


class BalanceSummaryStats(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )
    token_param = openapi.Parameter(
        "timegap",
        in_=openapi.IN_QUERY,
        description="Enter week/month/year to get records",
        type=openapi.TYPE_STRING,
    )

    @staticmethod
    def get_data(user, date):
        today_date = datetime.date.today()
        year_back = today_date - datetime.timedelta(days=12 * 30)
        month_back = today_date - datetime.timedelta(days=30)
        week_back = today_date - datetime.timedelta(days=7)

        income = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user)
        if date.lower() == "year":
            income = income.filter(
                credited_date__gte=year_back, credited_date__lte=today_date
            )
            expenses = expenses.filter(
                transaction_date__gte=year_back, transaction_date__lte=today_date
            )

        # Transaction from last month
        elif date.lower() == "month":
            income = income.filter(
                credited_date__gte=month_back, credited_date__lte=today_date
            )
            expenses = expenses.filter(
                transaction_date__gte=month_back, credited_date__lte=today_date
            )

        # Transaction from last week
        elif date.lower() == "week":
            income = income.filter(
                credited_date__gte=week_back, credited_date__lte=today_date
            )
            expenses = expenses.filter(
                transaction_date__gte=week_back, transaction_date__lte=today_date
            )
        sum = 0
        for ic in income:
            sum = sum + ic.amount
        for exp in expenses:
            sum = sum - exp.amount
        return sum

    @swagger_auto_schema(manual_parameters=[token_param])
    def get(self, request):

        date = request.GET.get("timegap", "")
        sum = BalanceSummaryStats.get_data(request.user, date)
        return response.Response({"Balance": sum}, status=status.HTTP_200_OK)


def send_alerts(user, user_alerts, data):
    if user_alerts.subscribe_to_email:
        response = Util.send_email(
            {
                "subject": data.get("subject", ""),
                "message": data.get("message", ""),
                "to_email": user.email,
            }
        )
        if response.get("status", "") == "success":
            Notifications.send_notification(bot_user, user, response.get("message", ""))
        elif response.get("status", "") == "error":
            Notifications.send_notification(
                bot_user,
                admin_user,
                response.get("message", "") + response.get("details", ""),
            )
            Notifications.send_notification(bot_user, user, response.get("message", ""))

    if user_alerts.subscribe_to_phone:
        # send_sms()
        response = send_sms(user.phonenumber, user.username,data.get("message",""))
        if response.get("status", "") == "success":
            Notifications.send_notification(user, user, response.get("message", ""))
        elif response.get("status", "") == "error":
            Notifications.send_notification(
                bot_user,
                admin_user,
                response.get("message", "") + response.get("details", ""),
            )
            Notifications.send_notification(bot_user, user, response.get("message", ""))


def prepare_alerts(user, date):
    user_alerts = Alert.objects.get(user=user)
    income, expense, balance = {}, {}, {}
    income["message"] = IncomeSummaryStats.get_data(user, date)
    expense["message"] = ExpenseSummaryStats.get_data(user, date)
    balance["message"] = BalanceSummaryStats.get_data(user, date)

    income["subject"] = user_alerts.income_summary_message
    expense["subject"] = user_alerts.expense_summary_message
    balance["subject"] = user_alerts.balance_summary_message
    content = [income, expense, balance]

    for data in content:
        send_alerts(user, user_alerts, data)
