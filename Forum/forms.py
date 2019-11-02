from django import forms
from Forum.models import *

class Forum_question_form(forms.ModelForm):
    
    class Meta:
        model = Forum_question
        fields = ('question','description')
        