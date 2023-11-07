from django.urls import re_path

from .views import home_page, view_list


urlpatterns = [
    re_path('^one-of-a-kind-list-in-the-world/$', view_list, name='view_list'),
    re_path('^$', home_page, name="home"),
]
