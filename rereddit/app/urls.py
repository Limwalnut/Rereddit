from django.urls import path
from django.conf.urls import *
from . import views
from django.conf import settings
from django.conf.urls.static import static


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
    url(r'^subscribe/(?P<operation>.+)/(?P<id>\d+)/$', views.subscribeTags, name='subscribeTags'),
    #url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^profile/(?P<id>[\w-]+)/$', views.profile_view, name='profile'),
    url(r'^profile/(?P<id>[\w-]+)/profile_update/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<id>[\w-]+)/change_password/$', views.change_passwords, name='change_password'),
    url(r'^(?P<id>[\w-]+)/$', views.thread_detail, name='thread_details'),
    url(r'^(?P<id>[\w-]+)/download/$', views.file_download, name='file_download'),
    url(r'^search/tags/(?P<name>[\w-]+)/$',views.search_tag, name='search_tag'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)