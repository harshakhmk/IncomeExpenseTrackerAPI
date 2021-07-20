from django.urls import reverse, path
from .views import *

urlpatterns = [
    path("category-expenses/", ExpenseSummaryStats.as_view(), name="category-expenses"),
    path("category-income/", IncomeSummaryStats.as_view(), name="category-income"),
    path("balance-summary/", BalanceSummaryStats.as_view(), name="balance-summary"),
]
