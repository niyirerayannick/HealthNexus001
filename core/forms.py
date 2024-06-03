from django import forms
from .models import Quiz, Question, Answer, Feedback,Course, User
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter Your Feedback'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.objects.get_teachers()

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']
        

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # Use the Question model here
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'})
        }


class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz')
        super(QuizForm, self).__init__(*args, **kwargs)
        for index, question in enumerate(quiz.questions.all(), start=1):
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=f"{index}. {question.text}",
                choices=[(answer.id, answer.text) for answer in question.answers.all()],
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
            )
