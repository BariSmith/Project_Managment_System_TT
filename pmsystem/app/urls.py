from django.urls import path
from . import views


urlpatterns = [
    path('projects/', views.projects, name='projects'),
    path('programmer/', views.programmer, name='programmer'),
    path('testing/', views.testing, name='testing'),
]
