from django.conf.urls import patterns, url

from blogengine import views

urlpatterns = patterns('',
    # Index url
    url(r'^$', views.IndexView.as_view(), name="index"),

    # Show url
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name="detail"),
)
