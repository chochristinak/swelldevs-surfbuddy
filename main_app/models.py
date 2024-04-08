from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField
    age = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.id})

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField
    age = models.IntegerField()
    students = models.ManyToManyField(Student)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'instructor_id': self.id})
    






