from django import forms
from .models import Quiz, Question, Answer
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']
        

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Answer
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
