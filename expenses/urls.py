from django.urls import path
from .views import *

urlpatterns = [
    path("expense-list/", ExpenseListView.as_view(), name="expense-list"),
    path("expense-detail/<int:id>", ExpenseDetailView.as_view(), name="expense-detail"),
    path("income-list/", IncomeListView.as_view(), name="income-list"),
    path("income-detail/<int:id>", IncomeDetailView.as_view(), name="income-detail"),
]
