from django.contrib import admin
from django.urls import path, include
from users.views import home, doubts, create_test, delete_quiz, class_detail, submit_answers, add_question_and_options, reels, profile, teacher_dashboard, student_dashboard, logout_view, create_class, join_class, teacher_signup, student_signup, generate_student_account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('logout/', logout_view, name='logout'),
    path('create_class/', create_class, name='create_class'),
    path('join_class/', join_class, name='join_class'),
    path('signup/teacher/', teacher_signup, name='teacher_signup'),
    path('signup/student/', student_signup, name='student_signup'),
    path('generate_student_account/<int:class_group_id>/', generate_student_account, name='generate_student_account'),
    path('reels/', reels, name='reels'),
    path('doubts/', doubts, name='doubts'),
    path('create_test/', create_test, name='create_test'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('add_question_and_options/<int:test_id>/', add_question_and_options, name='add_question_and_options'),
    path('reels/', reels, name='reels'),
    path('submit_answers/', submit_answers, name='submit_answers'),
    path('delete_quiz/<int:quiz_id>/', delete_quiz, name='delete_quiz'),
    path('class_detail/<int:class_id>/', class_detail, name='class_detail'),  # Add this line
    # path('delete_class/<int:class_id>/', delete_class, name='delete_class'),  # Add delete class URL

]
