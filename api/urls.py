from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    get_user, 
    EmployeeAttendanceViewSet, 
    EmployeeViewSet, 
    UserListView, 
    EmployeeDetailView, 
    LeaveRequestViewSet, 
    AdminLeaveRequestViewSet, 
    CustomTokenObtainPairView,
    LogoutView,
)

router = DefaultRouter()
router.register(r'attendances', EmployeeAttendanceViewSet, basename='attendance')
router.register(r'employees', EmployeeViewSet)
router.register(r'profile/leave-requests', LeaveRequestViewSet, basename='leave-request')
router.register(r'admin/leave-requests', AdminLeaveRequestViewSet, basename='admin-leave-request')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', get_user, name='get_user'),
    path('users/', UserListView.as_view(), name='user-list'),

    # User get token those endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('logout/', LogoutView.as_view(), name='logout'),


    path('employees/search/<int:user_id>/', EmployeeDetailView.as_view(), name='employee-search'),
]
