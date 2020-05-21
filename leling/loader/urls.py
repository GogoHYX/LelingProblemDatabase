from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:question_id>/result', views.detail, name='detail'),
    path('<int:question_id>/answer', views.answer, name='answer'),
    path('<int:question_id>/rubric', views.rubric, name='rubric'),
]