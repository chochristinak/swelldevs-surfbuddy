#-------------------- Module Imports --------------------
from django.urls import path
from . import views


#-------------------- Routes --------------------
urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('tidechart/', views.tidechart, name='tidechart'),
  path('lessons/', views.lessons_index, name='index'),
  path('lessons/<int:lesson_id>/', views.lessons_details, name='lessons_details'),
  path('lessons/create/', views.LessonCreate.as_view(), name='lessons_create'),
  path('lessons/<int:pk>/update/', views.LessonUpdate.as_view(), name='lessons_update'),
  path('lessons/<int:pk>/delete/', views.LessonDelete.as_view(), name='lessons_delete'),
  path('lessons/<int:lesson_id>/assoc_student/<int:student_id>/', views.assoc_student, name='assoc_student'),
  path('lessons/<int:lesson_id>/delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
  path('students/', views.StudentList.as_view(), name='students_index'),
  path('students/<int:pk>/', views.StudentDetail.as_view(), name='student_detail'),
  path('students/create/', views.StudentCreate.as_view(), name='students_create'),
  path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='students_update'),
  path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='students_delete'),
  path('accounts/signup/', views.signup, name='signup'),
  path('instructors/', views.instructors_index, name='instructors_index'),

  path('students/', views.LessonList.as_view(), name='students_index'),
]
