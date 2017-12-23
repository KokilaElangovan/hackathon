from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^mine/$', views.mine, name='mine'),
)
