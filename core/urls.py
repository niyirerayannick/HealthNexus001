from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    #course
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.view_course, name='view_course'),
    path('course/<int:course_id>/take/', views.take_course, name='take_course'),

    #quiz
    path('all-quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    
    #authentication
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    

    path('forget-password/', views.forget_password, name='forget_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    
    #dashboard
    path('student/dashboard/', views.Student_dashboard, name='my_dashboard'),
    path('student/courses/', views.student_courses, name='student_courses'),
    path('student/quizzes/', views.student_taken_quiz, name='student_quizzes'),
    path('student/check-marks/<int:quiz_id>/', views.check_marks_view, name='check_marks'),
    ]