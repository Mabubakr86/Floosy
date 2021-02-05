from django.shortcuts import render
from rest_framework import generics
from .serializers import WalletsSerialzer
from tracker.models import Wallet,Ticket

class WalletListCreateView(generics.ListCreateAPIView):
    serializer_class = WalletsSerialzer

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# class TicketListCreateView(generics.ListCreateAPIView):
#     serializer_class = TicketsSerialzer

#     def get_queryset(self):
#         user = self.request.user
#         wallets = Wallet.objects.filter(owner=user).values_list('id')
#         return Ticket.objects.filter(wallet_id__in=wallets)

#     # def perform_create(self, serializer):
#     #     serializer.save(wallet__owner=self.request.user)

#     def get_serializer_context(self):
#         return {'user': self.request.user}