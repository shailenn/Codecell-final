from django import forms
from Quiz.models import *
from Quiz.MultipleChoice.models import *
from django.forms.widgets import RadioSelect,CheckboxInput,TextInput

class QuizForm(forms.Form):

    def __init__(self, Current_quiz, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)

        Question_list = MCQ.objects.all().filter(quiz = Current_quiz).order_by("?")[:Current_quiz.max_questions]
        
        for i in range(len(Question_list)):
            Answer_choices = [ (x,x) for x in Answer.objects.all().filter(question = Question_list[i]).order_by('?')]
            if Question_list[i].single_correct:
                self.fields[Question_list[i].content] = forms.ChoiceField(choices = Answer_choices , widget = RadioSelect )
            else:
                self.fields[Question_list[i].content] = forms.ChoiceField(choices = Answer_choices , widget = CheckboxInput)
            
        
