from core.managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15,default=000000000000) 
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Student')


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    school = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user


class Course(models.Model):
    LEVEL_CHOICES = (
        ('1', 'Level One'),
        ('2', 'Level Two'),
        ('3', 'Level Three'),
    )

    name = models.CharField(max_length=100)
    course_banner = models.ImageField(upload_to='course_banner/')
    description = models.TextField()
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    category = models.CharField(max_length=100)
    content_image = models.ImageField(upload_to='course_images/')
    content_pdf = models.FileField(upload_to='course_pdfs/')
    content_video = models.FileField(upload_to='course_videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    related_quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True) 
    related_course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)  # ForeignKey to Quiz

    def __str__(self):
        return self.text

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

class CourseTaken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)