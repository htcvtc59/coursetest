from django.urls import path, re_path
from usersapp import views

urlpatterns = [
    path('mainpage/', views.usersappsignin, name='usersappsignin'),
]
