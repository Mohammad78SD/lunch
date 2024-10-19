from django.urls import include, path
from .views import attendance, attendance_list, change_attendance, user_requests

urlpatterns = [
    path('', attendance, name='attendance'),
    path('list/', attendance_list, name='attendance_list'),
    path('change/<int:attendance_id>/', change_attendance, name='change_attendance'),
    path('request/', change_attendance, name='request_attendance'),
    path('user-requests/', user_requests, name='user_requests'),


]