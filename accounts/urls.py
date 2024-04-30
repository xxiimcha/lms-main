from django.urls import path
from . import views

from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('login/',views.login_reader, name="login"),
    path('registration/',views.registration_reader,name="register"),

    path('password-reset/', PasswordResetView.as_view(template_name='accounts/password/password_reset.html'),name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='accounts/password/password_reset_complete.html'),name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.activate_email, name="email_verification"),
    path('password-change/', views.change_password, name="change_password_user"),
    # path('',views.index,name="home")
    # path('accounts/login/',views.login_view, name="login"),
    path('logout/', views.logout_reader, name="logout"),
    path('profile/dashboard/<str:pk>',views.profile_reader, name='profile'),
    path('profile/edit/<str:pk>',views.profile_edit, name="update-profile"),
    path('profile/reservation',views.reader_reservations, name="reservation-profile"),
    path('profile/<str:pk>/add-reservation',views.reader_makereservation, name="make_reservation"),
    path('profile/reservation/qrcode/<str:qrcode>', views.render_qrcode, name="render_qr")
]