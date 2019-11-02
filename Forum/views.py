from django.shortcuts import render
from Forum.models import *
from django.views.generic.edit import CreateView
from django.views import View
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse_lazy,reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

def forum_home(request, *args, **kwargs):
    No_of_questions_in_single_page = 25
    questions = Forum_question.objects.all().order_by('-asked_on')
    paginator = Paginator(questions, No_of_questions_in_single_page )

    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    return render(request,'Forum/Forum_home.html',{'question_list':question_list})

class Ask_question(View):
    template_name = "Forum/askquestion.html"

    def get(self, request, *args, **kwargs):
        ''' Process a get request for asking a question '''
        topic = Topic.objects.all()
        return render(request, self.template_name, {'topic':topic})

    def post(self, request, *args, **kwargs):
        ''' After a question is asked '''
        topic = request.POST.get('topic')
        question = request.POST.get('question')
        description = request.POST.get('description')
        if topic is not None and question is not None and description is not None:
            if question=="":
                return render(request, self.template_name, {"error":"Question cannot be blank","topic":Topic.objects.all()})
            new_question = Forum_question()
            new_question.question = question
            new_question.user = request.user
            new_question.description = description
            new_question.save()
            topic_list = Topic.objects.all().filter(title = topic)
            if topic_list:
                new_question.topic.add(*topic_list)
                new_question.save()
            return HttpResponseRedirect(reverse('forum_home'))
        return render(request, self.template_name, {"error":"There is a error in your form.","topic":Topic.objects.all()})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Add_answer(View):
    template_name = "Forum/answer_list.html"
    

    def get(self, request, *args, **kwargs):
        ''' Process a get request for answers '''
        question = Forum_question.objects.all().filter(pk = kwargs['pk'])[0]
        answers = Forum_answer.objects.all().filter(question = question).order_by('-answered_on')
        return render(request, self.template_name, {'answer':answers, 'question':question})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        ''' After a new answer is posted '''
        answer = request.POST.get('answer')
        question = Forum_question.objects.all().filter(pk = kwargs['pk'])[0]
        answers = Forum_answer.objects.all().filter(question = question).order_by('-answered_on')

        if answer is not None:
            if answer =="":
                blankerror = "Answer cannot be blank"
                return render(request, self.template_name, {'answer':answers,'question':question,'blankerror':blankerror})
            new_answer = Forum_answer.objects.create(answer = answer, question = question, user = request.user)
            return HttpResponseRedirect(reverse('answer_list', kwargs={'pk':question.pk}))
        return HttpResponseRedirect(reverse('answer_list'))

    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
