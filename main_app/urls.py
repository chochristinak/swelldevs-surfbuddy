#-------------------- Module Imports --------------------
from django.urls import path
from . import views


#-------------------- Routes --------------------
urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('lessons/', views.lessons_index, name='index'),
  path('lessons/<int:lesson_id>/', views.lessons_details, name='lessons_details'),
  path('lessons/create/', views.LessonCreate.as_view(), name='lessons_create'),
  path('lessons/<int:pk>/update/', views.LessonUpdate.as_view(), name='lessons_update'),
  path('lessons/<int:pk>/delete/', views.LessonDelete.as_view(), name='lessons_delete'),
  path('accounts/signup/', views.signup, name='signup'),

  path('students/', views.StudentList.as_view(), name='students_index'),
  path('lessons/<int:lesson_id>/assoc_student/<int:student_id>/', views.assoc_student, name='assoc_student'),
]
