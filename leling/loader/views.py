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
    func_dict = {
        'TF': __TFresult
    }
    return func_dict[question.type](request, question)


def __TFresult(request, question):
    ans = question.answer()
    score = 0
    if request.POST['choice'] == ans:
        score += 100
    return HttpResponse(str(score) + '%')


def interaction(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    func_dict = {
        'TF': __TFinteraction
    }
    return func_dict[question.type](request, question)


def __TFinteraction(request, question):
    template = loader.get_template('loader/TFinteraction.html')
    context = {
        'question': question,
        'stem': question.stem(),
    }
    return HttpResponse(template.render(context, request))


def with_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    template = loader.get_template('loader/question-index.html')
    context = {
        'question': question, }
    return HttpResponse(template.render(context, request))


def without_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    template = loader.get_template('loader/question-index.html')
    context = {
        'question': question, }
    return HttpResponse(template.render(context, request))

# helper methods
