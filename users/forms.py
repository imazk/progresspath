from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, TeacherProfile, StudentProfile

class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
            TeacherProfile.objects.create(user=user)  # Ensure profile is created here
        return user

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    grade = forms.CharField(max_length=10)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
            StudentProfile.objects.create(user=user, grade=self.cleaned_data['grade'])
        return user
    

from django import forms
from .models import ClassGroup

class CreateClassForm(forms.ModelForm):
    class Meta:
        model = ClassGroup
        fields = ['name', 'grade', 'subject', 'safe_mode', 'password']

from django import forms
from .models import ClassGroup

class JoinClassForm(forms.Form):
    name = forms.CharField()  # Add this field for filtering

    class_group = forms.ModelChoiceField(
        queryset=ClassGroup.objects.none(),  # Initially empty
        required=False
    )
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        super().__init__(*args, **kwargs)
        if name:
            self.fields['class_group'].queryset = ClassGroup.objects.filter(name__icontains=name)
        else:
            self.fields['class_group'].queryset = ClassGroup.objects.all()

class CreateStudentForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class_group = forms.ModelChoiceField(queryset=ClassGroup.objects.all(), required=True)

from django import forms
from .models import Test, Question, Option, DifficultyLevel

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'difficulty']
        widgets = {
            'difficulty': forms.Select(choices=Question.DIFFICULTY_CHOICES),
        }

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text', 'is_correct']


