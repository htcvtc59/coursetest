from django.urls import path, re_path
from usersapp import views

urlpatterns = [
    path('teacher/', views.usersappsignin, name='usersappsigninteacher'),
    path('student/', views.usersappsignin, name='usersappsigninstudent'),

    # teacher
    re_path('^teacher/course/getall/$', views.teachergetallcourse, name='teachergetallcourse'),
    # end teacher

    # evaluate student
    re_path('^teacher/student/evaluatestudent/$', views.teachercommentperstudent, name='teachercommentperstudent'),
    re_path('^teacher/student/getcomment/$', views.teachergetcomment, name='teachergetcomment'),
    # end evaluate student

    # upload file
    re_path('^teacher/course/loadsfile/$', views.teacherloadsfile, name='teacherloadsfile'),
    re_path('^teacher/course/teacheruploadfilessub/$', views.teacheruploadfilessub, name='teacheruploadfilessub'),
    re_path('^teacher/course/teacherdeletefile/$', views.teacherdeletefile, name='teacherdeletefile'),
    # end upload file

    # student
    re_path('^student/course/getallcourse/$', views.studentgetallcourse, name='studentgetallcourse'),
    re_path('^student/complete/$', views.studentcomplete, name='studentcomplete'),
    re_path('^student/course/studentgetallcoursecomplete/$', views.studentgetallcoursecomplete,
            name='studentgetallcoursecomplete'),
    re_path('^student/course/studentgetcoursefuture/$', views.studentgetcoursefuture, name='studentgetcoursefuture'),
    # end student
]
