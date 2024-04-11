#-------------------- Module Imports --------------------
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date


#-------------------- Constants --------------------
# locations to surf
BREAKS = (
    ('B', 'Beginner''s Bay'),
    ('S', 'Santana'),
    ('P', 'Popoyo'),
)

# skill level of students and surf locations
LEVELS = (
    ('B', 'Beginner'),
    ('I', 'Intermediate'),
    ('A', 'Advanced'),
    ('P', 'Pro'),
)


#-------------------- Models --------------------
# Student Model
class Student(models.Model):                                                                        
    name = models.CharField(max_length=100)                                                        # student name
    email = models.CharField(blank=True)                                                           # student email
    age = models.PositiveIntegerField(validators=[MinValueValidator(5), MaxValueValidator(110)])   # student age must positive and between the ages 5-110
    level = models.CharField(                                                                      # student skill level defaults to beginner
        default=LEVELS[0],
        choices=LEVELS,
    )

    # Foreign Key of the generic User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)                                       

    # returns the student name
    def __str__(self):
        return self.name

    # canonical URL of student object
    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.id})
    
# Instructor Model
class Instructor(models.Model):
    name = models.CharField(max_length=100)                                                        # instructor name  
    email = models.CharField(default='example@mail.com')                                                                      # instructor email
    age = models.IntegerField(default=15)                                                          # instructor age must be older than 15
    rating = models.IntegerField(default=5)                                                        # instructor rating
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    # Foreign Key of the generic User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)                                       

    # returns the instructor name and id
    def __str__(self):
        return f'{self.name} ({self.id})'

    # canonical URL of instructor object
    def get_absolute_url(self):
        return reverse('instructor_detail', kwargs={'pk': self.id})

# Lesson Model
class Lesson(models.Model):
    date = models.DateField()                                                                      # lesson date
    time = models.TimeField()                                                                      # lesson time
    level = models.CharField(                                                                      # lessons skill level
        default=LEVELS[0],
        choices=LEVELS,
    )
    location = models.CharField(                                                                   # lesson location
        choices=BREAKS,
    )

    # M:M relationship to student model
    student = models.ManyToManyField(Student)

    # M:M relationship to instructor model
    instructor = models.ManyToManyField(Instructor)

    # returns the lesson name and date
    def __str__(self):
        return f"{self.get_location_display()} on {self.date}"
    
    # canonical URL of lesson object
    def get_absolute_url(self):
        return reverse('lessons_details', kwargs={'lesson_id': self.id})
    
    # orders the lessons by time
    class Meta:
        ordering = ['time']

    # return the lessons for the current day
    def lesson_for_today(self):
        return self.lesson_set.filter(date=date.today()).count() >= len(BREAKS)
