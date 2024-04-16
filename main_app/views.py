#-------------------- Module Imports --------------------
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lesson, Student, Instructor
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path('.env'))


#-------------------- Functions --------------------
# Render the Home Page
def home(request):
  return render(request, 'home.html')

# Render the About Page
def about(request):
  return render(request, 'about.html')

# Render the Tide Chart Page and make an API Call to MArea API
def tidechart(request):
  # NOTE: comment out URL, headers, params, response, date, and extremes to make an API request
  # request URL to the Marea API
  URL = 'https://api.marea.ooo/v2/tides'

  # headers for the API request with the API key
  headers = {
    'x-marea-api-token': os.getenv('API_KEY')
  }

  # parameters needed to specify API data, these values can be changed
  params = {
    'latitude': 11.4701,                      # Popoyo Latitude
    'longitude': 86.1249,                     # Popoyo Longitude
    'datetime': '2024-04-15T00:05+00:00'      # date to see tides
  }

  # response data from the API call
  response = requests.get(URL, headers = headers, params = params).json()
  date = response['datetime']
  extremes = response['extremes']

  # full response data from API call NOTE: only print this to analyze the received data 
  # print(response)
  
  # Use this constant data for testing to reduce the number of times you retrieve data. The API only allows for 100 free requests
  # date = '2024-04-12T23:28:05+00:00'
  # extremes = [
  #   {
  #     'timestamp': 1712986780, 
  #     'height': 0.431819352, 
  #     'state': 'HIGH TIDE', 
  #     'datetime': '2024-04-13T05:39:40+00:00'
  #   }, 
  #   {
  #     'timestamp': 1713010066, 
  #     'height': -0.3024410408, 
  #     'state': 'LOW TIDE', 
  #     'datetime': '2024-04-13T12:07:46+00:00'
  #   }, 
  #   {
  #     'timestamp': 1713030492, 
  #     'height': 0.153368458, 
  #     'state': 'HIGH TIDE', 
  #     'datetime': '2024-04-13T17:48:12+00:00'
  #   }
  # ]
  
  # convert data heights and times to be more readable
  for e in extremes:
    # convert meters to feet
    e['height'] *= 3.281
    
    # if the value is negative, make it positive
    if (e['height'] < 0):
      e['height'] *= -1

    # format the heights to two decimal places
    e['height'] = "%.2f" % round(e['height'], 2)

    # det only the time from the datetime string
    e['datetime'] = e['datetime'][11:16]

  # save the time from the datetime string
  time = date[11:16]
   
  # render the Tide Chart Page with the data
  return render(request, 'tidechart.html', {
    'date': date[:10],
    'time': time,
    'extremes': extremes
  })

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
  # get all the lessons from the Lessons object
  lessons = Lesson.objects.all()

  # render the Lessons Index page
  return render(request, 'lessons/index.html', {
    'lessons': lessons
  })

# Render the Details Page for the specified Lesson
@login_required
def lessons_details(request, lesson_id):
  # get the current lesson from it's id
  lesson = Lesson.objects.get(id=lesson_id)

  # get the ids of the students in the current lesson
  id_list = lesson.student.all().values_list('id')

  # get all the students that are in the id list for the current lesson
  students = Student.objects.exclude(id__in=id_list)

  # get all ids of the instructors in the current lesson
  instructor_id_list = lesson.instructor.all().values_list('id')

  # get all the instructors that are in the id list for the current lesson
  instructors = Instructor.objects.exclude(id__in=instructor_id_list)

  # render the Lessons Details page
  return render(request, 'lessons/detail.html', {
    'lesson': lesson,
    'students': students,
    'instructors': instructors,
  })

# Create a Lesson
class LessonCreate(LoginRequiredMixin, CreateView):
  model = Lesson
  fields = ['date', 'time', 'level', 'location']
  success_url = '/lessons'

  # Determine if the form is valid
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

# Update a Lesson
class LessonUpdate(LoginRequiredMixin, UpdateView):
  model = Lesson
  fields = ['date', 'time', 'level', 'location']
  success_url = '/lessons'

# Delete a Lesson
class LessonDelete(LoginRequiredMixin, DeleteView):
  model = Lesson
  success_url = '/lessons'


#-------------------- Students --------------------
# Associate a student with a lesson
@login_required
def assoc_student(request, lesson_id, student_id):
  Lesson.objects.get(id=lesson_id).student.add(student_id)
  return redirect('lessons_details', lesson_id=lesson_id)

# Unassociate a student with a lesson
@login_required
def delete_student(request, lesson_id, student_id):
  Lesson.objects.get(id=lesson_id).student.remove(student_id)
  return redirect('lessons_details', lesson_id=lesson_id)

# Create a student
class StudentCreate(LoginRequiredMixin, CreateView):
  model = Student
  fields = '__all__'

# View the list of students
class StudentList(LoginRequiredMixin, ListView):
  model = Student

# Generate a detailed view of a student
class StudentDetail(LoginRequiredMixin, DetailView):
  model = Student

# Update the student information
class StudentUpdate(LoginRequiredMixin, UpdateView):
  model = Student
  fields = '__all__'

# Delete the student
class StudentDelete(LoginRequiredMixin, DeleteView):
  model = Student
  fields = '__all__'

# Delete the student
class StudentDelete(LoginRequiredMixin, DeleteView):
  model = Student
  success_url = '/students'


#-------------------- Instructors --------------------
# Render the Instructors Index Page with all the instructors
@login_required
def instructors_index(request):
  instructors = Instructor.objects.all()
  return render(request, 'instructors/index.html', {
    'instructors': instructors,
  })

# Associate an instructor with a lesson
@login_required
def assoc_instructor(request, instructor_id, lesson_id):
  Lesson.objects.get(id=lesson_id).instructor.add(instructor_id)
  return redirect( 'lessons_details', lesson_id=lesson_id)

# Unassociate an instructor with a lesson
@login_required
def delete_instructor(request, instructor_id, lesson_id):
  Lesson.objects.get(id=lesson_id).instructor.remove(instructor_id)
  return redirect('lessons_details', lesson_id=lesson_id)

# Create an instructor
class InstructorCreate(LoginRequiredMixin, CreateView):
  model = Instructor
  fields = '__all__'

# Show a list of the instructor details
class InstructorDetail(LoginRequiredMixin, DetailView):
  model = Instructor

# Update the instructor
class InstructorUpdate(LoginRequiredMixin, UpdateView):
  model = Instructor
  fields = '__all__'

# Delete the instructor
class InstructorDelete(LoginRequiredMixin, DeleteView):
  model = Instructor
  success_url = '/instructors'
