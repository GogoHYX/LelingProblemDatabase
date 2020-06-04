from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# Create your views here.
from django.template import loader
from django.views import generic

from .models import Question


class IndexView(generic.ListView):
    template_name = 'loader/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.order_by('-id')


def question_index(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    template = loader.get_template('loader/question-index.html')
    context = {
        'question': question, }
    return HttpResponse(template.render(context, request))


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    rub = question.rubric()

    return HttpResponse('')


def interaction(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    template = loader.get_template('loader/interaction.html')
    stem = question.stem()
    rub, ans_type = question.rubric()
    ans_type = [t.type.get_name_display() for t in ans_type]
    context = {
        'question': question,
        'stem': stem,
        'rubric': rub,
        'ans_type': ans_type,
    }
    return HttpResponse(template.render(context, request))


def with_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    template = loader.get_template('loader/with-answer.html')
    stem = question.stem()
    rub, ans_type = question.rubric()
    ans_type = [t.type.get_name_display() for t in ans_type]
    context = {
        'question': question,
        'stem': stem,
        'rubric': rub,
        'ans_type': ans_type,
    }
    return HttpResponse(template.render(context, request))


def without_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    template = loader.get_template('loader/without-answer.html')
    stem = question.stem()
    context = {
        'question': question,
        'stem': stem,
    }
    return HttpResponse(template.render(context, request))

# helper methods
