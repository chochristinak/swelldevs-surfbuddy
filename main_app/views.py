#-------------------- Module Imports --------------------
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm
from .models import Lesson, Student
from .forms import StudentForm


#-------------------- Functions --------------------
# Render the Home Page
def home(request):
  return render(request, 'home.html')

# Render the About Page
def about(request):
  return render(request, 'about.html')

# Render the Tide Chart page
def tidechart(request):
  return render(request, 'tidechart.html')

# Create a User from the information given and render the Signup Page
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


#-------------------- Lessons --------------------
# Render the Lessons Index Page with all the lessons in the database
def lessons_index(request):
  lessons = Lesson.objects.all()
  return render(request, 'lessons/index.html', {
    'lessons': lessons
  })

# Render the Details Page for the specified Lesson
def lessons_details(request, lesson_id):
  lesson = Lesson.objects.get(id=lesson_id)
  students = lesson.student.all()
  student_form = StudentForm()
  return render(request, 'lessons/detail.html', {
    'lesson': lesson,
    'students': students,
    'student_form': student_form
  })

def assoc_student(request, lesson_id, student_id):
  Lesson.objects.get(id=lesson_id).students.add(student_id)
  print("hello")
  return redirect('/lessons', lesson_id=lesson_id)

# Create a Lesson in the database using the CreateView Class
class LessonCreate(CreateView):
  model = Lesson
  fields = ['date', 'time', 'level', 'location']
  success_url = '/lessons'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

# Update a Lesson in the database using the UpdateView Class
class LessonUpdate(UpdateView):
  model = Lesson
  fields = ['date', 'time', 'level', 'location']
  success_url = '/lessons'

# Delete a Lesson in the database using the DeleteView Class
class LessonDelete(DeleteView):
  model = Lesson
  success_url = '/lessons'

#-------------------- Students --------------------
class StudentList(ListView):
  model = Student

class StudentCreate(CreateView):
  model = Student
  fields = '__all__'

class StudentDetail(DetailView):
  model = Student


#-------------------- Instructors --------------------
