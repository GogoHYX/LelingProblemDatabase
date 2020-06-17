from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.template import loader
from django.urls import reverse
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
    rubrics, ans_type = question.rubric()
    ans_type = [t.type.get_name_display() for t in ans_type]
    ans_list = []
    for i in range(len(rubrics)):
        ans = request.POST.getlist(str(i+1))
        ans_list.append(tuple(ans))
    score = question.grade_answer(ans_list)
    template = loader.get_template('loader/result.html')
    context = {
        'question': question,
        'score': score,
        'stem': question.stem(),
        'rubric': rubrics,
        'ans_type': ans_type,
        'ans_list': ans_list,
    }
    return HttpResponse(template.render(context, request))



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
