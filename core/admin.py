from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CourseForm
from .models import Course, Quiz, Question, Answer, User, UserProfile

class CourseAdmin(admin.ModelAdmin):
    form = CourseForm

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3  # Adjust this as per your requirement

class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1

class QuizQuestionAnswerInline(admin.TabularInline):
    model = Question
    fields = ['text']
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizQuestionAnswerInline]


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(Course, CourseAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Answer)
