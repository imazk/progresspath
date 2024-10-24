from django.urls import path
from .views import teacher_signup, student_signup, login_view, logout_view, teacher_dashboard, create_teacher_profile

urlpatterns = [
    path('signup/teacher/', teacher_signup, name='teacher_signup'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('create_teacher_profile/', create_teacher_profile, name='create_teacher_profile'),
    path('signup/student/', student_signup, name='student_signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
