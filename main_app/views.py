#-------------------- Module Imports --------------------
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
@login_required
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
@login_required
def lessons_index(request):
  lessons = Lesson.objects.all()
  return render(request, 'lessons/index.html', {
    'lessons': lessons
  })

# Render the Details Page for the specified Lesson
@login_required
def lessons_details(request, lesson_id):
  lesson = Lesson.objects.get(id=lesson_id)
  # students = lesson.student.all()
  id_list = lesson.student.all().values_list('id')
  students = Student.objects.exclude(id__in=id_list)
  student_form = StudentForm()
  return render(request, 'lessons/detail.html', {
    'lesson': lesson,
    'students': students,
    'student_form': student_form
  })

# Create a Lesson in the database using the CreateView Class
class LessonCreate(LoginRequiredMixin, CreateView):
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

# View the list of lessons
class LessonList(ListView):
  model = Lesson


#-------------------- Students --------------------
@login_required
def assoc_student(request, lesson_id, student_id):
  Lesson.objects.get(id=lesson_id).student.add(student_id)
  return redirect('lessons_details', lesson_id=lesson_id)

@login_required
def delete_student(request, lesson_id, student_id):
  Lesson.objects.get(id=lesson_id).student.remove(student_id)
  return redirect('lessons_details', lesson_id=lesson_id)

# View the list of students
class StudentList(ListView):
  model = Student

# Generate a detailed view of a student
class StudentDetail(DetailView):
  model = Student

# Create a student
class StudentCreate(CreateView):
  model = Student
  fields = '__all__'

class StudentDelete(DeleteView):
  model = Student
  fields = '__all__'

class StudentUpdate(UpdateView):
  model = Student
  fields = '__all__'

class StudentDelete(DeleteView):
  model = Student
  success_url = '/students'


#-------------------- Instructors --------------------
