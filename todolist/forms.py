from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from todolist.models import TaskList

class Taskform(forms.ModelForm):
    
    class Meta:
        model = TaskList
        fields = ['task','done']
class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name =forms.CharField(max_length=100)
    last_name  =forms.CharField(max_length=100)

    class meta:
        model=User
        fields =('username','first_name','last_name','email','password1','password2')