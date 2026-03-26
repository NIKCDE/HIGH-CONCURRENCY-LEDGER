from django.urls import path
from .views import CreateTransactionView, AccountListCreateView

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view()),
    path('transactions/', CreateTransactionView.as_view()),
]