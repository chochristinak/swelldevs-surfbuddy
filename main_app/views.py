from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from .models import Lesson, Instructor, Student


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
      error_message = 'Invalid'
    form = UserCreationForm()
    context = {'form':form, 'error_message': error_message }
    return render(request, 'registration/signup.html', context)

def instructors_index(request):
    return render(request, 'instructors/index.html')

def instructors_details(request):
    return render(request, 'instructors/details.html')

def students_index(request):
    return render(request, 'students/index.html')

def students_details(request):
    return render(request, 'students/details.html')

class LessonCreate(CreateView):
    model = Lesson
    fields = ['date', 'time', 'level', 'location']

class LessonUpdate(UpdateView):
    model = Lesson
    fields = ['date', 'time', 'level', 'location']

class LessonDelete(DeleteView):
    model = Lesson
    success_url ='/instructors/index'

class LessonList(ListView):
    model = Lesson
