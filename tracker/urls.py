from django.urls import path
from .views import *
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

app_name='tracker'

urlpatterns = [
    path('test/',TemplateView.as_view(template_name='tracker/index.html')),
    path('', WalletsView.as_view(), name='wallets'),
    path('add-wallet/',AddWalletView.as_view(),name='add_wallet'),
    path('wallet/<slug:slug>', wallet, name='wallet'),
    path('wallet/<slug:slug>/edit',EditWalletView.as_view(),name='edit_wallet'),
    path('wallet/<slug:slug>/delete',DeleteWalletView.as_view(),name='delete_wallet'),
    path('add-category/',AddCategoryView.as_view(), name='add_category'),
    path('stats/<slug:slug>/',stats, name='stats'),
    path('tickets/', tickets, name='tickets'),
    path('tickets/<slug:slug>/', wallettickets, name='wallet_tickets'),
    path('search/',ajax_search, name='search_tickets'),
    path('edit-ticket/<int:id>', edit_ticket,name='edit_ticket'),
    path('delete-ticket/<int:pk>', TicketDeleteView.as_view(),name='delete_ticket'),

]