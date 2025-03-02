from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from rest_framework.views import APIView
# from .Serializers import EmployeeSerializer
from .models import User,Employee
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .Serializers import RegisterSerializer, LoginSerializer, UserSerializer,DepartmentSerializer,DesignationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class EmployeeViews(APIView):
    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        employee = User.objects.all()
        serializer = UserSerializer(employee,many=True)
        return Response(serializer.data, status= 200)
    
class RegisterViews(generics.CreateAPIView):
    queryset=User.objects.all()
    permission_classes=[AllowAny]
    serializer_class=RegisterSerializer

class LoginViews(APIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email , password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh' : str(refresh),
                'access': str(refresh.access_token),
                'user':user_serializer.data
            })
        else:
            return Response({'detail': 'invalid credentials'})


class DesignationViews(APIView):
    def get(self, request):
        all_data = Employee.objects.all()
        designation_detail_serializer = DesignationSerializer(all_data , many=True)
        return Response(designation_detail_serializer.data)
    
class DepartmentViews(APIView):
    def get(self, request):
        all_data = Employee.objects.all()
        department_detail_serializer = DepartmentSerializer(all_data , many=True)
        return Response(department_detail_serializer.data)




