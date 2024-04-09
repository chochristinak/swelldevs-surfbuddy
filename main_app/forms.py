#-------------------- Module Imports --------------------
from django.forms import ModelForm
from .models import Lesson


#-------------------- Forms--------------------
# Lesson Form
class LessonForm(ModelForm):
  class Meta:
    model = Lesson
    fields = ['date', 'time', 'level','location']
