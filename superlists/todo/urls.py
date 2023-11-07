from django.urls import re_path

from .views import home_page, view_list, new_list


urlpatterns = [
    re_path('^$', home_page, name="home"),
    re_path('^new/$', new_list, name='new_list'),
    re_path('^one-of-a-kind-list-in-the-world/$', view_list, name='view_list'),
]
