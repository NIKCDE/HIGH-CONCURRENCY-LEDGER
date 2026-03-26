from rest_framework import serializers
from .models import Account, Transaction, Entry

class EntrySerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=["DEBIT", "CREDIT"])
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)


class TransactionSerializer(serializers.Serializer):
    reference = serializers.CharField()
    entries = EntrySerializer(many=True)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"