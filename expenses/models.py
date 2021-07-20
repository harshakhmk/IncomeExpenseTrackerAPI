from django.db import models
from authenticate.models import User

# Create your models here.


class Expense(models.Model):
    expense_choices = [
        ("Travel", "Travel"),
        ("Food", "Food"),
        ("Shopping", "Shopping"),
        ("Basic Needs", "Basic Needs"),
        ("Petrol", "Petrol"),
        ("Gifts", "Gifts"),
        ("Sports", "Sports"),
        ("Clothes", "Clothes"),
        ("Entertainment", "Entertainment"),
        ("Others", "Others"),
    ]
    category = models.CharField(max_length=50, choices=expense_choices)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-transaction_date"]

    def __str__(self):
        return f"{str(self.user.username)} spent {self.amount} on {self.category} "

    def expense_summary_message(self, timestamp):
        return (
            f"Hello {self.user.username} this {timestamp}, here are your expense stats"
        )


class Income(models.Model):
    income_choices = [
        ("Income", "Income"),
        ("Bonus", "Bonus"),
        ("Side Husttle", "Side Husttle"),
        ("Others", "Others"),
    ]
    category = models.CharField(max_length=50, choices=income_choices)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credited_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-credited_date"]

    def __str__(self):
        return f"{str(self.user.username)} spent {self.amount} on {self.category} "
