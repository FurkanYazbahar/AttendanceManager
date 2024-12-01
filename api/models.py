from django.db import models
from datetime import datetime, date
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    parent_department = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_departments'
    )  # Hiyerarşik yapı için, bir departmanın üst departmanını belirtir.

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )  # Çalışanın yöneticisini belirtir.
    hire_date = models.DateField()  # Şirkete giriş tarihi
    termination_date = models.DateField(null=True, blank=True)  # Çıkış tarihi
    annual_leave_days = models.FloatField(default=15)  # Yıllık izin
    annual_leave_used = models.FloatField(default=0)  # Kullanılmış yıllık izin
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    performance_rating = models.FloatField(null=True, blank=True)
    overtime_hours = models.FloatField(null=True, default=0)
    work_schedule = models.CharField(max_length=100, default='08:00-18:00')
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username


class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField()  # Tarih
    entry_time = models.TimeField()  # Giriş Saati
    end_time = models.TimeField(null=True)  # Çıkış Saati
    delayed_time = models.DurationField(null=True)  # Gecikme Süresi

    class Meta:
        verbose_name = "Employee Attendance"
        verbose_name_plural = "Employee Attendances"

    def __str__(self):
        return f"Attendance for {self.employee.user.username} on {self.date}"


class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def leave_days(self):
        return (self.end_date - self.start_date).days + 1