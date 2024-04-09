from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date

# Create your models here.

BREAKS = (
    ('B', 'Beginner''s Bay'),
    ('S', 'Santana'),
    ('P', 'Popoyo'),
)

LEVELS = (
    ('B', 'Beginner'),
    ('I', 'Intermediate'),
    ('A', 'Advanced'),
    ('P', 'Pro'),
)

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField
    age = models.PositiveIntegerField(validators=[MinValueValidator(5), MaxValueValidator(110)])
    level = models.CharField(
        default=LEVELS[0],
        choices=LEVELS,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.id})
    

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField
    age = models.IntegerField(default=15)
    rating = models.IntegerField(default=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'instructor_id': self.id})


class Lesson(models.Model):
    date = models.DateField()
    time = models.TimeField()
    level = models.CharField(
        default=LEVELS[0],
        choices=LEVELS,
    )
    location = models.CharField(
        choices=BREAKS,
    )
    student = models.ManyToManyField(Student)
    instructor = models.ManyToManyField(Instructor)

    def __str__(self):
        return f"{self.get_location_display()} on {self.date}"
    
    def get_absolute_url(self):
        return reverse('lessons_details')
    
    class Meta:
        ordering = ['time']

    def lesson_for_today(self):
        return self.lesson_set.filter(date=date.today()).count() >= len(BREAKS)
    



    
