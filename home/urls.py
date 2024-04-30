from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name='home'),
    path('about/',views.about, name='about'),
    path('menu/',views.menu,name="home_menu"),
    path('services/',views.services, name='home_services')
]