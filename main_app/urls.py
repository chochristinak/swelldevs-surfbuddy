from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('accounts/signup/', views.signup, name='signup'),
  path('instructors/details/', views.instructors_details, name='instructors_details'),
  path('instructors/index/', views.instructors_index, name='instructors_index'),
  path('students/index/', views.students_index, name='students_index'),
  path('students/details/', views.students_details, name='students_details'),
]