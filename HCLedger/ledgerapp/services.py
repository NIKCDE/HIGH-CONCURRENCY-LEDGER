from django.db import transaction
from .models import Account, Transaction, Entry
from decimal import Decimal
from .models import IdempotencyKey
from django.core.exceptions import ObjectDoesNotExist


class LedgerService:
    @staticmethod
    @transaction.atomic
    def create_transaction(reference, entries_data, idempotency_key=None):
        #STEP 0: Check idempotency
        if idempotency_key:
            try:
                existing = IdempotencyKey.objects.get(key=idempotency_key)
                if existing.response_data:
                    return existing.response_data  #Return previous response
            except ObjectDoesNotExist:
                pass

        #Balance validation
        total_debit = Decimal("0.00")
        total_credit = Decimal("0.00")

        for entry in entries_data:
            amount = Decimal(entry["amount"])
            if entry["type"] == "DEBIT":
                total_debit += amount
            else:
                total_credit += amount
        if total_debit != total_credit:
            raise ValueError("Transaction must be balanced")
        txn = Transaction.objects.create(reference=reference)
        for entry in entries_data:
            account = Account.objects.select_for_update().get(id=entry["account_id"])
            amount = Decimal(entry["amount"])
            Entry.objects.create(
                transaction=txn,
                account=account,
                entry_type=entry["type"],
                amount=amount
            )
            if entry["type"] == "DEBIT":
                account.balance += amount
            else:
                account.balance -= amount

            account.save(update_fields=["balance"])
        response = {"message": "Transaction successful", "reference": reference}

        #Save idempotency record
        if idempotency_key:
            IdempotencyKey.objects.create(
                key=idempotency_key,
                response_data=response
            )
        return response
    
