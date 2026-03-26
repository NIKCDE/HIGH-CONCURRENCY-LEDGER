from django.db import models
from decimal import Decimal

class Account(models.Model):
    ACCOUNT_TYPES = (
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('EQUITY', 'Equity'),
    )

    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    reference = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Entry(models.Model):
    ENTRY_TYPE = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    )

    transaction = models.ForeignKey(Transaction, related_name='entries', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.entry_type} - {self.amount}"
    
class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    response_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)