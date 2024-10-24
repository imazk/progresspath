from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TeacherProfile, StudentProfile, ClassGroup

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Roles', {'fields': ('is_teacher', 'is_student')}),
    )


class ClassGroupAdmin(admin.ModelAdmin):
    list_filter = ('name',)  # Filter by class group name
    search_fields = ('name',)  

admin.site.register(User, UserAdmin)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(ClassGroup, ClassGroupAdmin)

from django.contrib import admin
from .models import Test, Question, Option, DifficultyLevel

class OptionInline(admin.TabularInline):
    model = Option

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(DifficultyLevel)

