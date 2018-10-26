from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    # path(r'', views.index, name='index'),
    # path(r'getdata', views.getdata, name='getdata')
    path(r'', views.toppage),
    path(r'abc', views.search_and_result),
    path(r'lecture', views.lecture, name='lecture'),
    path(r'department', views.department_page, name='department'),
    path(r'base_layout', views.base_layout, name='base_layout'),
]
