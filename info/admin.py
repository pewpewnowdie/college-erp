from django.contrib import admin
from .models import User, Department, Program, Course, Student, Teacher, Attendance, StudentCourse, Exam, Assignment, TeacherCourse
# Register your models here.

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(StudentCourse)
admin.site.register(TeacherCourse)
admin.site.register(Exam)
admin.site.register(Assignment)
admin.site.register(Attendance)
