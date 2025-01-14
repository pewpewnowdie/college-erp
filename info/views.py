from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from info.models import StudentCourse, Attendance, Course, Student
from info.forms import TeacherAttendanceForm

User = get_user_model()

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
    if request.user.is_student:
        student = request.user.student
        student_courses = StudentCourse.objects.filter(student=student)
        att_list = []
        for student_course in student_courses:
            att_list.append({'course': student_course.course, 'attendance': student_course.get_attendance()})
        return render(request, 'info/s_attendance.html', {'att_list': att_list})
    elif request.user.is_teacher:
        teacher = request.user.teacher
        if request.method == 'POST':
            form = TeacherAttendanceForm(request.POST, teacher=teacher)
            if form.is_valid():
                date = form.cleaned_data['date']
                course = form.cleaned_data['course']
                return redirect(reverse('info:attendance_list', kwargs={'course_id': course.id, 'date': date}))
        else:
            form = TeacherAttendanceForm(teacher=teacher)
            return render(request, 'info/t_attendance.html', {'form': form})
    return render(request, 'landing.html')


@login_required
def attendance_list(request, course_id, date):
    if request.user.is_teacher:
        course = Course.objects.get(id=course_id)
        studentcourses = StudentCourse.objects.filter(course=course)
        students = Student.objects.filter(id__in=studentcourses.values('student_id')).distinct()
        if request.method == 'POST':
            for student in students:
                is_present = request.POST.get(f'attendance_{student.id}') == 'on'
                Attendance.objects.update_or_create(
                    studentcourse=StudentCourse.objects.get(student=student, course=course), date=date,
                    defaults={'status': is_present}
                )
            return redirect('info:attendance')

        return render(request, 'info/t_attendance_list.html', {
            'course': course,
            'date': date,
            'students': students
        })
    render(request, 'landing.html')
