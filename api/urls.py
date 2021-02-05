from django.urls import path, include
from .views import *


app_name = 'api'

urlpatterns = [
    path('', WalletListCreateView.as_view(), name='api_wallet_list_create'),
    # path('tickets/', TicketListCreateView.as_view(), name='api_ticket_list_create'),


]