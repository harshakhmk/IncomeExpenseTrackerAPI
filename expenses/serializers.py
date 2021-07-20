from rest_framework import serializers
from .models import *


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("id", "category", "amount", "description", "transaction_date")


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ("id", "category", "amount", "description", "credited_date")
