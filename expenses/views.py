from django.shortcuts import render
from .serializers import *
from .models import *

# Create your views here.
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from utils.permission import *


class ExpenseListView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

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
