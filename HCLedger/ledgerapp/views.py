from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TransactionSerializer, AccountSerializer
from .models import Account
from .services import LedgerService


class CreateTransactionView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                txn = LedgerService.create_transaction(
                    reference=serializer.validated_data["reference"],
                    entries_data=serializer.validated_data["entries"]
                )
                return Response({"message": "Transaction successful"}, status=201)
            except ValueError as e:
                return Response({"error": str(e)}, status=400)
        return Response(serializer.errors, status=400)


class AccountListCreateView(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)