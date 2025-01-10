from django.db import models
from django.contrib.auth.models import AbstractUser

exam_choices = (
    ('mid', 'mid'),
    ('end', 'end'),
    ('back', 'back'),
)

class User(AbstractUser):
    @property
    def is_student(self):
        if hasattr(self, 'student'):
            return True
        return False

    @property
    def is_teacher(self):
        if hasattr(self, 'teacher'):
            return True
        return False

class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    uni_rno = models.CharField(max_length=20, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(default=1)
    contact_no = models.CharField(max_length=15, unique=True, null=True, blank=True)
    DOB = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.uni_rno}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15, unique=True, null=True, blank=True)
    DOB = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.designation}"

class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
    
class TeacherCourse(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "course"], name="unique_teacher_course"
            )
        ]
    
    def __str__(self):
        return f"{self.teacher} - {self.course}"

class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"], name="unique_student_course"
            )
        ]
    
    def __str__(self):
        return f"{self.student} - {self.course}"

    def get_attendance(self):
        attendance_records = Attendance.objects.filter(studentcourse=self)
        total_attendance = attendance_records.count()
        present_attendance = attendance_records.filter(status=True).count()
        return {
            "total": total_attendance,
            "present": present_attendance,
            "percentage": round(present_attendance / total_attendance * 100, 2) if total_attendance > 0 else 0
        }

    def get_marks(self):
        exam_records = Exam.objects.filter(studentcourse=self)
        mid_records = exam_records.filter(type='mid')
        end_records = exam_records.filter(type='end')
        mid = mid_records.first().marks if mid_records.exists() else 0
        end = end_records.first().max_marks if end_records.exists() else 0
        mid_tot = mid_records.first().marks if mid_records.exists() else 0
        end_tot = end_records.first().max_marks if end_records.exists() else 0
        return {
            'mid': mid,
            'mid_tot': mid_tot,
            'end': end,
            'end_tot': end_tot
        }

class Attendance(models.Model):
    studentcourse = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["studentcourse", "date"], name="unique_attendance"
            )
        ]
    
    def __str__(self):
        return f"{self.studentcourse} - Date {self.date} - {self.status}"

class Exam(models.Model):
    studentcourse = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=exam_choices)
    marks = models.PositiveIntegerField()
    max_marks = models.PositiveIntegerField(default=100)
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["studentcourse", "type"], name="unique_exam"
            )
        ]

    def __str__(self):
        return f"{self.studentcourse} - {self.marks}/{self.max_marks}"

    
class Assignment(models.Model):
    studentcourse = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    max_marks = models.PositiveIntegerField(default=100)
    date_of_assignment = models.DateField()
    date_of_submission = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["studentcourse", "date_of_assignment"], name="unique_assignment"
            )
        ]

    def __str__(self):
        return f"{self.studentcourse} - {self.marks} / {self.max_marks}"
