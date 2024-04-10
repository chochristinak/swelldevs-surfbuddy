#-------------------- Module Imports --------------------
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Lesson


#-------------------- Functions --------------------
# Render the Home Page
def home(request):
  return render(request, 'home.html')

# Render the About Page
def about(request):
  return render(request, 'about.html')

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

  return render(request, 'lessons/detail.html', {
    'lesson': lesson,
  })

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



#-------------------- Instructors --------------------
