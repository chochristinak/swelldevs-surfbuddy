from django.contrib import admin
from .models import Instructor, Student, Lesson

# Register your models here.

admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Lesson)