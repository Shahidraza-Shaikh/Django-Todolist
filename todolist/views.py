from django.shortcuts import render ,redirect
from todolist.models import TaskList
from todolist.forms import Taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate ,login , logout
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from bs4  import BeautifulSoup
import requests
# Create your views here. 
def todolist(request): 
    if request.method == 'POST':
        form = Taskform(request.POST , None)
        if form.is_valid():
            form.save()
        messages.success(request,'New Task is Added Successfully at last page!!')
        return redirect('todolist')
    else: 

        all_tasks = TaskList.objects.all()
        paginator =Paginator(all_tasks ,8)
        page= request.GET.get('pg')
        all_tasks =paginator.get_page(page)
         
        return render(request,'todolist.html', {'all_tasks':all_tasks})

def delete_task(request ,task_id):
    task=TaskList.objects.get(pk=task_id)
    task.delete()
    return redirect('todolist')
def edit_task(request, task_id):
    if request.method == 'POST':
        task=TaskList.objects.get(pk=task_id)
        form=Taskform(request.POST or None ,instance=task)
        if form.is_valid():
            form.save()
        messages.success(request,'Task Edited')
        return redirect('todolist')
    else: 
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request,'edit.html', {'task_obj':task_obj})


def contact(request):
    context ={
        'contact_text':"Welcome  To Contact Page",
    }
    return render(request,'contact.html',context)


def index(request):
    context ={
        'index_text':"Welcome To Home Page",
    }
    return render(request,'index.html',context)


def about(request):
    '''context ={
        'about_text':"Welcome To About Us Page",
    }
    '''
    sourcce= requests.get('http://quotes.toscrape.com/page/2/').text

    Soup= BeautifulSoup(sourcce, 'lxml')
    # print(Soup)
    # li=[]
    titles =Soup.find_all(class_='text')
    # for i in range(len(titles)):
    #     li.append[titles[i].text]
    context={}
    for i in range(len(titles)):
        context[i] = titles[i].text
        # li.append[context]
    return render(request,'about.html',context)

def complete_task(request ,task_id):
    task=TaskList.objects.get(pk=task_id)
    task.done =True  
    task.save()
    return redirect('todolist')
def pending_task(request ,task_id):
    task=TaskList.objects.get(pk=task_id)
    task.done =False 
    task.save()
    return redirect('todolist')

def login_user(request):
    if request.method == 'POST':
        username= request.POST['username']
        password=request.POST['password']
        user = authenticate(request ,username=username ,password =password)
        if user is not  None:
            login(request, user)
            messages.success(request, ('You are login successfully !'))
            return redirect('index')
        else :
            messages.success(request, ('Error login in - Please try Again !'))
            return redirect('login')
    else :

        return render(request ,'login.html' ,{})
def logout_user(request):
    messages.success(request, ('You have been Logout !'))
    logout(request)
    return redirect('login')
def register_user(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user =authenticate(username=username,password=password)
            messages.success(request,'You have been Register')
            return redirect('index')
    else :
        form =SignUpForm()
    context={'form':form}
    return render(request ,'register.html',context)