from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    contact_no = models.CharField(max_length=15, unique=True, null=True, blank=True)
    DOB = models.DateField()
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
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
    name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
    name = models.CharField(max_length=100, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    uni_rno = models.CharField(max_length=20, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.uni_rno}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.designation}"

class CourseClass(models.Model):  # Renamed to avoid conflict with 'class'
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(default=1)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.name} - Semester {self.semester}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_class = models.ForeignKey(CourseClass, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course_class", "date"], name="unique_attendance"
            )
        ]