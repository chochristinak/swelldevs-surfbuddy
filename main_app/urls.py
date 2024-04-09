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

  path('lessons/create/', views.LessonCreate.as_view(), name='lessons_create'),
  path('lessons/<int:pk>/update/', views.LessonUpdate.as_view(), name='lessons_update'),
  path('lessons/<int:lesson_id>/delete/', views.LessonDelete.as_view(), name='lessons_delete'),
  path('lessons/index/', views.LessonList.as_view(), name='lessons_index'),
  path('lessons_details', views.LessonDetail.as_view(), name='lessons_details'),
  path('lessons/<int:lesson_id>/details', views.LessonDetail.as_view(), name='lesson_detail')
]
