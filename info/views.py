from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model
from info.forms import CustomUserCreationForm
from info.models import Student, StudentCourse

User = get_user_model()
# Create your views here.

@login_required
def index(request):
    if request.user.is_teacher:
        return render(request, 'info/t_homepage.html')
    if request.user.is_student:
        return render(request, 'info/s_homepage.html')
    return render(request, 'landing.html')

class LandingPageView(TemplateView):
    template_name = "landing.html"

@login_required
def attendance(request):
    if not request.user.is_student:
        return render(request, 'landing.html')
    student = request.user.student
    student_courses = StudentCourse.objects.filter(student=student)
    att_list = []
    for student_course in student_courses:
        att_list.append({'course' : student_course.course, 'attendance' : student_course.get_attendance()})
    return render(request, 'info/s_attendance.html', {'att_list' : att_list})