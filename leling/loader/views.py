from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic

from ..uploader.models import Question

class IndexView(generic.ListView):
    template_name = 'loader/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-id')[:5]

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
