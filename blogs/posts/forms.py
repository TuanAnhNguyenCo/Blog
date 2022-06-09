from django import forms
from .models import Answers,Questions

class AnswerForm(forms.ModelForm):
    class Meta:
        model  = Answers
        fields = ['answer',"images"]
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model  = Questions
        fields = ['powerteam','title','description','images']
        

