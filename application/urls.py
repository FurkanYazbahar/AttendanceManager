from django.urls import path, include
from . import views

#router = DefaultRouter()
#router.register(r'Employee', EmployeeViewSet)
#router.register(r'attendance', AttendanceViewSet)
#router.register(r'leaverequests', LeaveRequestViewSet)attendance

urlpatterns = [
    #path('', include(router.urls)),leave_request
    #path('', views.index, name='index'),
    path('login/', views.login, name='login'),    
    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('user/profile/', views.profile, name='profile'),
    path('employee/attendance/', views.employee_attendance, name='employee_attendance'),
    path('employee/management/', views.employee_leave_management, name='employee_leave_management'),
    path('employee/information/', views.employee_information, name='employee_information'),

    path('profile/leave/request', views.leave_request, name='leave_request'),
     path('admin/leave/request', views.leave_management, name='leave_management'),       
]