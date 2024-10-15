from django.urls import include, path
from .views import attendance, attendance_list

urlpatterns = [
    path('', attendance, name='attendance'),
    path('list/', attendance_list, name='attendance_list'),
]