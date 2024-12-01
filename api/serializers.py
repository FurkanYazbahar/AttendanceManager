from datetime import time, datetime, timedelta
from django.utils.timezone import now, localtime, make_aware
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Employee, EmployeeAttendance, LeaveRequest, Department, Position


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'is_active']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'description', 'parent_department']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['name', 'description']


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer()  # Departman ismini göstermek için
    position = PositionSerializer()  # Pozisyon ismini göstermek için
    #manager = serializers.StringRelatedField()  # Yönetici adını göstermek için

    class Meta:
        model = Employee
        fields = [
            'id',            
            'user',
            'department',
            'position',            
            'hire_date',
            'termination_date',
            'annual_leave_days',
            'annual_leave_used',
            'salary',
            'performance_rating',
            'overtime_hours',
            'work_schedule',
            'email',
            'phone',
        ]


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.username', read_only=True)

    class Meta:
        model = EmployeeAttendance
        fields = ['id', 'employee', 'employee_name', 'date', 'entry_time', 'end_time', 'delayed_time']


class LeaveRequestSerializer(serializers.ModelSerializer):
    leave_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveRequest
        fields = ['id', 'start_date', 'end_date', 'reason', 'status', 'leave_days']
        read_only_fields = ['status', 'leave_days']  # `status` genelde yönetici tarafından güncellenir 'employee_id',

class AdminLeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        try:
            employee = Employee.objects.get(user=user)
            today = now().date()

            # İstemciden gelen UTC saatini backend'in lokal zamanına dönüştür
            entry_time = now()  # Giriş saati (UTC)
            localized_entry_time = localtime(entry_time).time()  # Lokal zamana dönüştür

            expected_start_time = time(8, 0)  # İşe başlama saati (lokal zaman)
            delayed_time = timedelta(0)

            if localized_entry_time > expected_start_time:
                delayed_time = datetime.combine(today, localized_entry_time) - datetime.combine(today, expected_start_time)

            if not EmployeeAttendance.objects.filter(employee=employee, date=today).exists():
                EmployeeAttendance.objects.create(
                    employee=employee,
                    date=today,
                    entry_time=localized_entry_time,
                    delayed_time=delayed_time,
                )
        except Employee.DoesNotExist:
            pass
        return data