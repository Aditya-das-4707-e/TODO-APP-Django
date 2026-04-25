from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.task_creat, name='task_creat'),
    path('edit/<int:pk>/', views.task_updat, name='task_updat'),
    path('delete/<int:pk>/', views.task_delet, name='task_delet'),
    path('done/<int:pk>/', views.task_toggle, name='task_toggle'),
]