from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.message_list, name='messages_list'),
]
