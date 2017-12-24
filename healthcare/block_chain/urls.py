from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^notify/$', views.get_notified, name='get-notified'),
    url(r'^add_record/$', views.add_record, name='add-record'),
    url(r'^get_record/$', views.get_user_records, name='get-user-records'),
    url(r'^join/$', views.join_request, name='join-request'),
)
