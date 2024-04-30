from django.urls import path
from . import views
from .views import AdminPasswordResetView,AdminPasswordResetDoneView, AdminPasswordResetConfirmView, AdminPasswordResetCompleteView

# from django.contrib.auth.views import (
#     LogoutView, 
#     PasswordResetView, 
#     PasswordResetDoneView, 
#     PasswordResetConfirmView,
#     PasswordResetCompleteView
# )



urlpatterns = [
    path('', views.admin_index, name='admin_index'),
    path('login/', views.admin_login, name="admin_login"),
    path('logout',views.admin_logout,name="admin_logout"),
    path('add_staff/',views.admin_addstaff, name="admin_add_staff"),
    path('list_staff/',views.admin_staff_list, name="admin_staff_list"),
    path('add_classification',views.admin_add_book_classification, name="admin_add_classification"),
    path('add_book/',views.admin_add_book, name="admin_add_book"),
    path('list_book/',views.admin_book_list, name="admin_book_list"),
    path('list_reservation/',views.admin_reservation_list, name="admin_reservation_list"),
    path('approved_reservation/<str:pk>',views.approve_reservation, name="approved_reservation"),
    path('declined_reservation/<str:pk>',views.decline_reservatioon, name="declined_reservation"),
    # path('borrowed_reservation/test',views.borrowed_reserved,name="borrowed_reservation"),
    path('borrow_books/',views.borrow_books, name="book_borrow_list"),
    path('return_book_borrowed/<str:pk>',views.return_book,name="return_book_borrowed"),
    path('reservation/scan_qr/', views.scan_qr_page, name="scan_qr"),
    path('search_qr/reservation',views.search_qr, name="search_qr"),
    path('book_borrow_info/<str:qr>', views.get_borrow_info_book, name="borrow_info_book"),
    path('return_book_reservation/<str:pk>', views.return_books_from_reservation, name="return_book_reservation"),
    path('borrow_book_walkin/', views.borrow_book_walkin, name="borrow_book_walkin"),
    path('search_book/', views.get_book_info_walk, name="search_book"),
    path('borrow_book_walkin/', views.get_book_borrowed, name="borrowed_books"),
    
    path('change_password/',views.account_settings, name="change_password"),


    path('admin-password-reset/', AdminPasswordResetView.as_view(), name='admin_password_reset'),
    path('admin-password-reset-done/', AdminPasswordResetDoneView.as_view(), name="admin_password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', AdminPasswordResetConfirmView.as_view(),name='admin_password_reset_confirm'),
    path('password-reset-complete/',AdminPasswordResetCompleteView.as_view(),name='admin_password_reset_complete'),
    
]