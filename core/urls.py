from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('how-it-work/', views.how_it_work, name='how-it-work'),
    path('about/', views.about, name='about-us'),
    path('feedback/',views.feedback, name='feedback'),
    path('feedback-confirm/',views.feed_confirm, name='feedback-confirm'),
    path('terms-and-conditions/',views.terms, name='terms-and-conditions'),
    path('privacy-policy/',views.privacy, name='privacy-policy'),
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
    
    #dashboard student
    path('student/dashboard/', views.Student_dashboard, name='my_dashboard'),
    path('student/courses/', views.student_courses, name='student_courses'),
    path('student/quizzes/', views.student_taken_quiz, name='student_quizzes'),
    path('student/check-marks/<int:quiz_id>/', views.check_marks_view, name='check_marks'),
    #dashboard student
    #dashboard teacher
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/courses/', views.teacher_courses, name='teacher_courses'),
    path('teacher/courses/<int:course_id>/', views.teacher_course_detail, name='teacher_course_detail'),
    path('teacher/quizzes/', views.teacher_quizzes, name='teacher_quizzes'),
    path('teacher/quizzes/<int:quiz_id>/', views.teacher_quiz_detail, name='teacher_quiz_detail'),
]