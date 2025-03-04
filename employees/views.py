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
from django.conf import settings
import boto3

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


# THIS API WILL GIVE THE ITEMS PRESENT IN THE S3 BUCKET

class S3BucketView(APIView):
   s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
    )
   def get(self,request):
            #access all the bucket names
            s3_bucket = self.s3_client.list_buckets()
            # s3_bucket_name = s3_bucket['Buckets']  
            s3_bucket_names = [bucket_name['Name'] for bucket_name in s3_bucket.get('Buckets' , [])] 

            #access content of the buckets
            Content = {}
            for s3_bucket_name in s3_bucket_names:
                s3_content = self.s3_client.list_objects_v2(Bucket = s3_bucket_name)
                Content[s3_bucket_name] = [contents['Key'] for contents in s3_content.get('Contents' , [])]

            return Response({
                "Bucket_name":s3_bucket_name,
                "Content": Content
            })


     
