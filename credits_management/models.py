from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class UserCredits(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='credits')
    total_credits = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.total_credits} credits"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'Credit Addition'),
        ('OUT', 'Credit Deduction'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} {self.amount} credits"


class CreditValue(models.Model):
    value_per_credit = models.DecimalField(max_digits=10, decimal_places=2)
    date_effective = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"R$ {self.value_per_credit} per credit (effective {self.date_effective})"


class EndpointPricing(models.Model):
    endpoint = models.CharField(max_length=255, unique=True)
    cost_in_credits = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.endpoint} - {self.cost_in_credits} credits"
