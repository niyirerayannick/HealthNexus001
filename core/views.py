# core/views.py
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from HealthNexus import settings
from core.forms import FeedbackForm, QuizForm
from .models import Answer, Course, CourseTaken, Quiz, QuizResult, User
from .tokens import account_activation_token
from django.contrib.auth.forms import PasswordResetForm 
from django.utils.encoding import force_str
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse
from .models import User 

User = get_user_model()

def home(request):
    quizzes = Quiz.objects.all()
    courses = Course.objects.all()
    context ={'quizzes': quizzes,'courses': courses}
    return render(request, 'home/home.html', context)

def how_it_work(request):
    return render(request, 'home/how_it_work.html')

def about(request):
    return render(request, 'admin/about.html')

def feed_confirm(request):
    return render(request, 'home/feedback_confirm.html')

@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback-confirm')
    else:
        form = FeedbackForm()
    return render(request, 'home/feedback.html', {'form': form})

def terms(request):
    return render(request, 'home/terms.html')

def privacy(request):
    return render(request, 'home/policy.html')

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    form = QuizForm(request.POST or None, quiz=quiz)
    
    if request.method == 'POST':
        if form.is_valid():
            score = 0
            total = quiz.questions.count()
            for question in quiz.questions.all():
                answer_id = form.cleaned_data.get(f'question_{question.id}')
                if answer_id:
                    answer = Answer.objects.get(id=answer_id)
                    if answer.is_correct:
                        score += 1
            
            # Calculate percentage score
            percentage_score = (score / total) * 100
            
            # Render quiz result
            return render(request, 'quiz/quiz_result.html', {'quiz': quiz, 'score': score, 'total': total, 'percentage_score': percentage_score})
    
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'form': form})

def course_list(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'course/course_list.html', context)

def view_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'course/take_course.html', {'course': course})

@login_required
def take_course(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    CourseTaken.objects.get_or_create(user=user, course=course)
    return redirect('view_course', pk=course_id)

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        telephone = request.POST['telephone']
        password = request.POST['password']
        
        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return redirect(reverse('register'))  # Redirect to registration page
        
        # Check if telephone is already registered
        if User.objects.filter(telephone=telephone).exists():
            messages.error(request, 'This telephone number is already registered.')
            return redirect(reverse('register'))  # Redirect to registration page

        # Create inactive user
        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, telephone=telephone, is_active=False)
        
        # Send verification email
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string('admin/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(subject, message, 'niyannick120@gmail.com', [user.email])
        
        return redirect('account_activation_sent')
    else:
        return render(request, 'admin/registration.html')
    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # Specify the backend explicitly
        backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user, backend=backend)
        return redirect('home')
    else:
        return render(request, 'admin/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'admin/account_activation_sent.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to dashboard or any other page
        else:
            # Authentication failed
            messages.error(request, 'Invalid email or password')
            return render(request, 'admin/login.html')
    else:
        return render(request, 'admin/login.html')

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Generate token for password reset
            token = default_token_generator.make_token(user)

            # Build reset password link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.BASE_URL}/reset-password/{uid}/{token}/"

            # Send password reset email
            subject = 'Reset Your Password'
            message = render_to_string('admin/reset_password_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            return render(request, 'admin/password_reset_response.html', {'message': "Password reset link sent to your email."})
        else:
            return render(request, 'admin/password_reset_response.html', {'message': "No user found with this email."})
    else:
        return render(request, 'admin/forget_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST['password']
            user.password = make_password(password)
            user.save()
            login(request, user)
            return redirect('home')  # Redirect to home page after resetting password
        else:
            return render(request, 'admin/reset_password.html')
    else:
        return HttpResponse('Invalid password reset link.')

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('home')  # Redirect to home page after logout
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
    

@login_required
def Student_dashboard(request):
    user = request.user
    total_courses_taken = CourseTaken.objects.filter(user=user).count()
    total_quizzes_taken = QuizResult.objects.filter(user=user).count()
    latest_quiz_result = QuizResult.objects.filter(user=user).order_by('-date_taken').first()
    quiz_results = QuizResult.objects.filter(user=user)
    courses_taken = CourseTaken.objects.filter(user=user)

    context = {
        'quiz_results': quiz_results,
        'courses_taken': courses_taken,
        'user':user,
        'total_courses_taken': total_courses_taken,
        'total_quizzes_taken': total_quizzes_taken,
        'latest_quiz_result': latest_quiz_result,
    }
    return render(request, 'student/student_dashboard.html', context)

@login_required
def student_courses(request):
    user = request.user
    courses_taken = CourseTaken.objects.filter(user=user).select_related('course')

    context = {
        'courses': courses_taken,
    }

    return render(request, 'student/student_courses.html', context)



@login_required
def student_taken_quiz(request):
    user = request.user
    quizzes_taken = QuizResult.objects.filter(user=user).select_related('quiz')

    context = {
        'quizzes': quizzes_taken,
    }

    return render(request, 'student/student_quiz.html', context)

@login_required
def check_marks_view(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    quiz_results = QuizResult.objects.filter(user=user, quiz__course=course)

    context = {
        'course': course,
        'quiz_results': quiz_results,
    }

    return render(request, 'student/student_results.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Course, Quiz, QuizResult, User, CourseTaken

@login_required
def teacher_dashboard(request):
    user = request.user
    courses_taught = Course.objects.filter(teacher=user)
    total_courses_taught = courses_taught.count()
    quizzes_taught = Quiz.objects.filter(course__teacher=user)
    total_quiz = quizzes_taught.count()
    total_students = User.objects.filter(coursetaken__course__in=courses_taught).distinct().count()
    latest_quiz_results = QuizResult.objects.filter(quiz__course__in=courses_taught).order_by('-date_taken')[:5]

    context = {
        'total_quiz':total_quiz,
        'quizzes_taught': quizzes_taught,
        'courses_taught': courses_taught,
        'total_courses_taught': total_courses_taught,
        'total_students': total_students,
        'latest_quiz_results': latest_quiz_results,
    }
    return render(request, 'teacher/teacher_dashboard.html', context)

@login_required
def teacher_courses(request):
    user = request.user
    courses_taught = Course.objects.filter(teacher=user)

    context = {
        'courses_taught': courses_taught,
    }

    return render(request, 'teacher/teacher_courses.html', context)

@login_required
def teacher_course_detail(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    context = {
        'course': course,
    }

    return render(request, 'teacher/teacher_course_detail.html', context)

@login_required
def teacher_quizzes(request):
    user = request.user
    quizzes_taught = Quiz.objects.filter(course__teacher=user)

    context = {
        'quizzes_taught': quizzes_taught,
    }

    return render(request, 'teacher/teacher_quizzes.html', context)

@login_required
def teacher_quiz_detail(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)

    context = {
        'quiz': quiz,
    }

    return render(request, 'teacher/teacher_quiz_detail.html', context)
