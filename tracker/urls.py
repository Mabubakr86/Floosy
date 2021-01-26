from django.urls import path
from .views import *

from django.contrib.auth.views import LoginView

app_name='tracker'

urlpatterns = [
    path('', WalletsView.as_view(), name='wallets'),
    path('add-wallet/',AddWalletView.as_view(),name='add_wallet'),
    path('wallet/<slug:slug>', wallet, name='wallet'),
    path('wallet/<slug:slug>/edit',EditWalletView.as_view(),name='edit_wallet'),
    path('wallet/<slug:slug>/delete',DeleteWalletView.as_view(),name='delete_wallet'),
    path('add-category/',AddCategoryView.as_view(), name='add_category'),
    path('stats/',stats, name='stats'),
    path('tickets/', tickets, name='tickets'),
]