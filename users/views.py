from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import User
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import TeacherProfile, StudentProfile, ClassGroup
from .forms import CreateClassForm, JoinClassForm
from .models import Test, Question, Option
from .forms import TestForm, QuestionForm, OptionForm
from django.db import IntegrityError
from .forms import TeacherSignUpForm, StudentSignUpForm, CreateClassForm, JoinClassForm, TestForm, QuestionForm, OptionForm
from .models import User, TeacherProfile, StudentProfile, ClassGroup, Test, Question, Option
from datetime import datetime


from django.shortcuts import render, get_object_or_404
from .models import ClassGroup

@login_required
def class_detail(request, class_id):
    class_group = get_object_or_404(ClassGroup, id=class_id)
    return render(request, 'class_detail.html', {'class_group': class_group})


@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Test, id=quiz_id)
    quiz.delete()
    return redirect('teacher_dashboard')


def login_view(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        password = request.POST.get('password')

        if '@' in email_or_username:
            try:
                user_queryset = User.objects.filter(email=email_or_username)
                if user_queryset.count() > 1:
                    return render(request, 'users/login.html', {'error': 'Multiple accounts found. Please use your username to log in.'})
                user = user_queryset.first()
                username = user.username
            except User.DoesNotExist:
                username = email_or_username
        else:
            username = email_or_username

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('student_dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username/email or password'})
    return render(request, 'users/login.html')

@login_required
def create_class(request):
    if request.user.is_teacher:
        if request.method == 'POST':
            form = CreateClassForm(request.POST)
            if form.is_valid():
                class_group = form.save(commit=False)
                class_group.teacher = request.user.teacherprofile
                class_group.save()
                return redirect('teacher_dashboard')
        else:
            form = CreateClassForm()
        return render(request, 'create_class.html', {'form': form})
    else:
        return redirect('home')

@login_required
def join_class(request):
    name = request.GET.get('name', None)
    if request.user.is_student:
        if request.method == 'POST':
            form = JoinClassForm(request.POST, name=name)
            if form.is_valid():
                class_group = form.cleaned_data['class_group']
                password = form.cleaned_data['password']
                if class_group.password == password or not class_group.password:
                    class_group.students.add(request.user.studentprofile)
                    return redirect('student_dashboard')
                else:
                    form.add_error('password', 'Incorrect password')
        else:
            form = JoinClassForm(name=name)
        return render(request, 'join_class.html', {'form': form})
    else:
        return redirect('home')

@login_required
def generate_student_account(request, class_group_id):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username=username).exists():
                return render(request, 'generate_student_account.html', {
                    'error': 'A user with that username already exists.',
                    'class_group_id': class_group_id
                })
            user = User.objects.create_user(username=username, email=email, password=password)
            # Mark the user as a student
            user.is_student = True
            user.save()
            student_profile = StudentProfile(user=user)
            student_profile.save()
            class_group = ClassGroup.objects.get(id=class_group_id)
            class_group.students.add(student_profile)
            class_group.save()
            return redirect('teacher_dashboard')
        except IntegrityError:
            return render(request, 'generate_student_account.html', {
                'error': 'There was an error creating the student account. Please try again.',
                'class_group_id': class_group_id
            })
    else:
        return render(request, 'generate_student_account.html', {'class_group_id': class_group_id})


def home(request):
    return render(request, 'home.html')

def reels(request):
    questions = Question.objects.prefetch_related('options').all()
    return render(request, 'reels.html', {'questions': questions})

def doubts(request):
    return render(request, 'doubts.html')

def profile(request):
    return render(request, 'profile.html')

@login_required
def student_dashboard(request):
    current_date = datetime.now().strftime("%d %b %Y")
    return render(request, 'student_dashboard.html', {'current_date': current_date})

def logout_view(request):
    logout(request)
    return redirect('home')

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                if not TeacherProfile.objects.filter(user=user).exists():
                    TeacherProfile.objects.create(user=user)
                return redirect('login')
            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}")  # Add a non-field error
        else:
            print("Form is not valid:", form.errors)
    else:
        form = TeacherSignUpForm()
    return render(request, 'users/signup_form.html', {'form': form})

# @login_required
# def teacher_dashboard(request):
#     if request.user.is_teacher:
#         if request.method == 'POST':
#             test_form = TestForm(request.POST)
#             if test_form.is_valid():
#                 test_form.save()
#                 return redirect('teacher_dashboard')
#             else:
#                 print("Form is not valid:", test_form.errors)
#         else:
#             test_form = TestForm()
#         class_groups = request.user.teacherprofile.class_groups.all()
#         tests = Test.objects.all()
#         return render(request, 'teacher_dashboard.html', {
#             'test_form': test_form,
#             'tests': tests,
#             'class_groups': class_groups
#         })
#     else:
#         return redirect('home')


# @login_required
# def teacher_dashboard(request):
#     if not hasattr(request.user, 'teacherprofile'):
#         TeacherProfile.objects.create(user=request.user)
#     class_groups = request.user.teacherprofile.class_groups.all()
#     return render(request, 'teacher_dashboard.html', {'class_groups': class_groups})

@login_required
def teacher_dashboard(request):
    if request.user.is_teacher:
        # Ensure TeacherProfile exists
        if not hasattr(request.user, 'teacherprofile'):
            TeacherProfile.objects.create(user=request.user)
        
        if request.method == 'POST':
            test_form = TestForm(request.POST)
            if test_form.is_valid():
                test_form.save()
                return redirect('teacher_dashboard')
            else:
                print("Form is not valid:", test_form.errors)
        else:
            test_form = TestForm()
        
        class_groups = request.user.teacherprofile.class_groups.all()
        tests = Test.objects.all()
        return render(request, 'teacher_dashboard.html', {
            'test_form': test_form,
            'tests': tests,
            'class_groups': class_groups
        })
    else:
        return redirect('home')


@login_required
def create_teacher_profile(request):
    if not hasattr(request.user, 'teacherprofile'):
        TeacherProfile.objects.create(user=request.user)
    return redirect('teacher_dashboard')

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = StudentSignUpForm()
    return render(request, 'users/signup_form.html', {'form': form})

def class_group_list(request):
    name = request.GET.get('name', None)
    if name:
        class_groups = ClassGroup.objects.filter(name__icontains=name)
    else:
        class_groups = ClassGroup.objects.all()
    return render(request, 'class_group_list.html', {'class_groups': class_groups})

@login_required
def create_test(request):
    if request.user.is_teacher:
        if request.method == 'POST':
            test_form = TestForm(request.POST)
            if test_form.is_valid():
                test = test_form.save()
                return redirect('add_question_and_options', test_id=test.id)
            else:
                print("Form is not valid:", test_form.errors)
        else:
            test_form = TestForm()
        return render(request, 'create_test.html', {'test_form': test_form})
    else:
        return redirect('home')

@login_required
def add_question_and_options(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_forms = [OptionForm(request.POST, prefix=str(i)) for i in range(4)]
        if question_form.is_valid() and all(form.is_valid() for form in option_forms):
            question = question_form.save(commit=False)
            question.test = test
            question.save()
            for form in option_forms:
                option = form.save(commit=False)
                option.question = question
                option.save()
            return redirect('add_question_and_options', test_id=test.id)
    else:
        question_form = QuestionForm()
        option_forms = [OptionForm(prefix=str(i)) for i in range(4)]
    return render(request, 'add_question_and_options.html', {
        'question_form': question_form,
        'option_forms': option_forms,
        'test': test
    })


def submit_answers(request):
    if request.method == 'POST':
        score = 0
        total_questions = Question.objects.count()

        for question in Question.objects.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                if selected_option.is_correct:
                    score += 1
        
        return render(request, 'reels.html', {
            'questions': Question.objects.all(),
            'score': score,
            'total_questions': total_questions,
        })
    return redirect('reels')
