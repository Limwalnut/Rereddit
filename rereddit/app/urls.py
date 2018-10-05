from django.urls import path
from django.conf.urls import *
from . import views


app_name = 'app'


urlpatterns = [
    path('',views.index, name='home'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$',views.logout_view, name='logout'),
    url(r'^index/$', views.index, name='index'),
    url(r'^threads/$', views.thread_list, name='threads'),
    url(r'^create/$', views.thread_create, name='create'),
    url(r'^result/$', views.search_result, name='result'),
    url(r'^(?P<id>[\w-]+)/$', views.thread_detail, name='thread_details'),

]