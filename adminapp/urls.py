from django.urls import path, re_path
from adminapp import views

urlpatterns = [
    path('app/', views.adminbasecourse, name='adminbasecourse'),
    path('app/users/', views.adminbaseaccount, name='adminbaseaccount'),
    path('app/students/', views.adminbasestudents, name='adminbasestudents'),
    path('app/session/', views.adminappsession, name='adminappsession'),

    # teacher
    re_path('^app/appteacher/getall/$', views.appteachergetall, name='appteachergetall'),
    re_path('^app/appteacher/create/$', views.appteachercreate, name='appteachercreate'),
    re_path('^app/appteacher/delete/$', views.appteacherdelete, name='appteacherdelete'),
    re_path('^app/appteacher/update/$', views.appteacherupdate, name='appteacherupdate'),
    # end teacher

    # student
    re_path('^app/appstudent/getall/$', views.appstudentgetall, name='appstudentgetall'),
    re_path('^app/appstudent/create/$', views.appstudentcreate, name='appstudentcreate'),
    re_path('^app/appstudent/delete/$', views.appstudentdelete, name='appstudentdelete'),
    re_path('^app/appstudent/update/$', views.appstudentupdate, name='appstudentupdate'),
    # end student

    re_path('^app/category/$', views.appcategory, name='appcategory'),
    re_path('^app/category/create/$', views.appcategorycreate, name='appcategorycreate'),
    re_path('^app/category/getdata/$', views.appcategorygetdata, name='appcategorygetdata'),
    re_path('^app/category/delete/$', views.appcategorydelete, name='appcategorydelete'),
    re_path('^app/category/getnav/$', views.appcategorygetnav, name='appcategorygetnav'),

    re_path('^app/category/(?:root-(?P<rootname>[A-Za-z]+)/)?$', views.appcategoryrootname, name='appcategoryrootname'),
    re_path('^app/category/(?:sub-(?P<subname>[A-Za-z]+)/)?$', views.appcategorysubname, name='appcategorysubname'),

    # student detail
    re_path('^app/appstudentinfo/getall/$', views.adminstudentsgetall, name='adminstudentsgetall'),
    re_path('^app/appstudentinfo/create/$', views.adminstudentscreate, name='adminstudentscreate'),
    re_path('^app/appstudentinfo/delete/$', views.adminstudentsdelete, name='adminstudentsdelete'),
    re_path('^app/appstudentinfo/update/$', views.adminstudentsupdate, name='adminstudentsupdate'),
    # end student detail

    # course
    re_path('^app/category/(?:sub-(?P<subname>[A-Za-z]+)/(?P<info>[A-Za-z0-9]+))?$', views.coursegetinfosub,
            name='coursegetinfosub'),
    re_path('^app/category/(?:root-(?P<rootname>[A-Za-z]+)/(?P<info>[A-Za-z0-9]+))?$', views.coursegetinforoot,
            name='coursegetinforoot'),

    re_path('^app/appcourse/getallpagination/$', views.coursegetallsearch, name='coursegetallsearch'),
    re_path('^app/appcourse/coursegetstudentin/$', views.coursegetstudentin, name='coursegetstudentin'),

    re_path('^app/appcourse/create/$', views.createcourse, name='createcourse'),
    re_path('^app/appcourse/delete/$', views.deletecourse, name='deletecourse'),
    re_path('^app/appcourse/update/$', views.updatecourse, name='updatecourse'),
    # end course

]
