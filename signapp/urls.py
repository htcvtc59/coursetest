from django.urls import path
from signapp import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),

]
