from django.shortcuts import render
from .serializers import *
from .models import *
from authenticate.models import *
# Create your views here.
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from utils.permission import *
from utils.notifications import Notifications
admin_user = User.objects.all().filter(is_superuser=True)
bot_user = User.objects.get(email="botIETeam@gmail.com")
class ExpenseListView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):

        response =  serializer.save(user=self.request.user)
        income = Income.objects.filter(user=self.request.user)
        expenses = Expense.objects.filter(user=self.request.user)
        sum = 0
        for ic in income:
            sum = sum + ic.amount
        for exp in expenses:
            sum = sum - exp.amount
        if(sum<=0):
            bot_user = self.request.user
            Notifications.send_notification(bot_user, user, f"Dear {self.request.user.username} your balance has reached {sum}, spend your expenses wisely")
        return response

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    lookup_field = "id"
    serializer_class = ExpenseSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class IncomeListView(ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class IncomeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    lookup_field = "id"
    serializer_class = IncomeSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
