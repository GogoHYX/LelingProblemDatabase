from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('multiple-choice/', views.multiple_choice, name='multiple_choice'),
    path('multiple-choice/add', views.add, name='add'),
]