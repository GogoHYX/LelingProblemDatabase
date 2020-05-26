from django.urls import path

from . import views

app_name = 'loader'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:question_id>/', views.question_index, name='question_index'),
    path('<int:question_id>/interaction', views.interaction, name='interaction'),
    path('<int:question_id>/with-answer', views.with_answer, name='with-answer'),
    path('<int:question_id>/without-answer', views.without_answer, name='without-answer')
]