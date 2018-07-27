from django.urls import path, re_path
from usersapp import views

urlpatterns = [
    path('teacher/', views.usersappsignin, name='usersappsigninteacher'),
    path('student/', views.usersappsignin, name='usersappsigninstudent'),

    # teacher
    re_path('^teacher/course/getall/$', views.teachergetallcourse, name='teachergetallcourse'),
    # end teacher


]
