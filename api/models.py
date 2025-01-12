from django.db import models


class Account(models.Model):
    account_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_id} - {self.name}"
