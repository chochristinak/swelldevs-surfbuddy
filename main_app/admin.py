#-------------------- Module Imports --------------------
from django.contrib import admin
from .models import Instructor, Student, Lesson


#-------------------- Model Registration --------------------
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Lesson)
