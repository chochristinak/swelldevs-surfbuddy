#-------------------- Module Imports --------------------
from django.forms import ModelForm
from .models import Lesson, Student, Instructor
from django.contrib.auth.forms import UserCreationForm, forms


#-------------------- Forms--------------------
# Lesson Form
class LessonForm(ModelForm):
  class Meta:
    model = Lesson
    fields = ['date', 'time', 'level', 'location']

# Student Form
class StudentForm(ModelForm):
  class Meta:
    model = Student
    fields = ['name', 'email', 'age', 'level']

class InstructorForm(ModelForm):
  class Meta:
    model = Instructor
    fields = ['name', 'email', 'age', 'rating']

class StudentUserCreationForm(UserCreationForm):
    USERNAME_FIELD = forms.CharField(label="Username")
    name = forms.CharField(label="name")
    email = forms.EmailField(label="email")
    age = forms.CharField(label="age")
    level = forms.CharField(label="level")

    class Meta:
      model = Student
      fields = ("name", "email", "age", "level")
    
    def save(self, commit=True):
      user = super(StudentUserCreationForm, self).save(commit=False)
      if commit:
        user.save()
      return user