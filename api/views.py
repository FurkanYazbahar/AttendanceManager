from django.utils.timezone import localtime, now
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Employee, EmployeeAttendance, LeaveRequest
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from .serializers import ( 
    EmployeeSerializer, 
    EmployeeAttendanceSerializer, 
    LeaveRequestSerializer, 
    UserSerializer, 
    AdminLeaveRequestSerializer, 
    CustomTokenObtainPairSerializer
)
from .paginations import DataTablePagination

#class EmployeeListCreateAPIView(generics.ListCreateAPIView):
#    queryset = Employee.objects.all()
#    serializer_class = EmployeeSerializer
#    #permission_classes = [permissions.IsAuthenticated]

# User List View
class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    pagination_class = DataTablePagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'is_active']

class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            employee = Employee.objects.get(user_id=user_id)  # user_id üzerinden çalışanı bulun
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=200)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)
        

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    #permission_classes = [IsAuthenticated]

class EmployeeAttendanceViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAttendance.objects.all()
    serializer_class = EmployeeAttendanceSerializer
    pagination_class = DataTablePagination  # Pagination sınıfını ekledik
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['employee__user__username', 'date']  # Aranabilir alanlar
    ordering_fields = ['date', 'entry_time', 'end_time']  # Sıralama yapılabilir alanlar
    ordering = ['date']  # Varsayılan sıralama
    #permission_classes = [IsAuthenticated]

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    pagination_class = DataTablePagination  # Pagination sınıfını ekledik
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['start_date', 'end_date', 'reason', 'status']  # Aranabilir alanlar
    ordering_fields = ['start_date', 'end_date']  # Sıralama yapılabilir alanlar
    ordering = ['start_date']  # Varsayılan sıralama
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Sadece oturum açmış kullanıcının izin taleplerini göster
        user = self.request.user
        if hasattr(user, 'employee'):
            return LeaveRequest.objects.filter(employee=user.employee)
        return LeaveRequest.objects.none()

    def perform_create(self, serializer):
        # İzin talebi oluştururken `employee`yi otomatik ekle
        serializer.save(employee=self.request.user.employee)

class AdminLeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = AdminLeaveRequestSerializer
    pagination_class = DataTablePagination  # Pagination sınıfını ekledik
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['start_date', 'end_date', 'reason', 'status']  # Aranabilir alanlar
    ordering_fields = ['start_date', 'end_date']  # Sıralama yapılabilir alanlar
    ordering = ['start_date']  # Varsayılan sıralama
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Sadece giriş yapmış kullanıcılar erişebilir
def get_user(request):
    user = request.user
    # Kullanıcının ilk grubunun adını al
    role = user.groups.first().name
    print(role)
    return Response({
        'username': user.username,
        'email': user.email,
        'role': role,
        'user_id': user.id
    })


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Çalışanı al
            employee = Employee.objects.get(user=request.user)
            today = now().date()  # UTC tarih

            # Kullanıcıya ait bugünkü kaydı al
            attendance = EmployeeAttendance.objects.filter(employee=employee, date=today).first()

            if attendance:
                # Lokal saat ile çıkış zamanını güncelle
                localized_time = localtime(now()).time()  # Lokal zamana dönüştür
                #print(f"localtime : {localized_time}")
                attendance.end_time = localized_time
                attendance.save()

            return Response({"detail": "Logout successful, attendance updated."}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_400_BAD_REQUEST)