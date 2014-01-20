from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.ProfileView.as_view(), name='detail'),
    url(r'^edit/$', views.ProfileEdit.as_view(), name='edit'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
)
