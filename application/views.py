from django.shortcuts import render

# Create your views here.


def login(request):
    return render(request, 'application/login.html')

#def index(request):
#    return render(request, 'application/index.html')

#def index(request):
#
#    # Page from the theme 
#    return render(request, 'pages/dashboard.html')

def dashboard(request):
    return render(request, 'application/dashboard.html')

def profile(request):
    return render(request, 'application/profile.html')

def leave_request(request):
    return render(request, 'application/leave_request.html')

def leave_management(request):
    return render(request, 'application/leave_management.html')

def employee_attendance(request):
    return render(request, 'application/employee_attendance.html')

def employee_leave_management(request):
    return render(request, 'application/employee_leave_management.html')

def employee_information(request):
    return render(request, 'application/employee_information.html')

