#-------------------- Module Imports --------------------
from django.forms import ModelForm
from .models import Lesson, Student


#-------------------- Forms--------------------
# Lesson Form
class LessonForm(ModelForm):
  class Meta:
    model = Lesson
    fields = ['date', 'time', 'level','location']

# Student Form
class StudentForm(ModelForm):
  class Meta:
    model = Student
    fields = ['name', 'email', 'age', 'level']
