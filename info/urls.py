from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'info'

urlpatterns = [
    path('', views.index, name="index"),
    path('attendance/', views.attendance, name="attendance"),
    path('attendance_list/<int:course_id>/<str:date>/', views.attendance_list, name='attendance_list'),
]
