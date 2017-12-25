from django.conf.urls import patterns, url
import views, models

urlpatterns = patterns('',
    url(r'^notify/$', views.get_notified, name='get-notified'),
    url(r'^add_record/$', views.new_record, name='add-record'),
    url(r'^get_record/$', views.get_user_records, name='get-user-records'),
    url(r'^public_key/$', views.get_public_key, name='add-record'),
    url(r'^join/$', views.join_request, name='join-request'),
)
