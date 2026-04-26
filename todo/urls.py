from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('done/<int:pk>/', views.task_toggle, name='task_toggle'),
]