from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .views import signup, edit_profile
from django.views.generic import TemplateView
from django.contrib.auth.views import (PasswordResetView,PasswordResetDoneView,
    PasswordResetConfirmView,)

app_name = 'accounts'


urlpatterns = [
    path('login/',LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name='accounts/logout.html'),name='logout'),
    path('signup/', signup, name='signup'),
    path('profile/', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),  
    path('edit-profile/', edit_profile, name='edit_profile'),

    path('password-reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html'), name ='password_reset'),
    path('password-reset/sent/', PasswordResetDoneView.as_view(template_name = "accounts/password_reset_done.html"), name ='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name ='password_reset_confirm'),

]


