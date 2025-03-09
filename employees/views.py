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
    def post(self, request):
        all_data = Employee.objects.all()
        input_designation=request.data.get('designation')
        designations=Employee.objects.filter(designation=input_designation)
        if input_designation is not None:
            designation_detail_serializer = DesignationSerializer(designations, many=True)
            return Response(designation_detail_serializer.data)
        designation_detail_serializer = DesignationSerializer(all_data , many=True)
        return Response(designation_detail_serializer.data)
    
class DepartmentViews(APIView):
    def post(self, request):
        all_data = Employee.objects.all()
        input_department=request.data.get('department')
        department=Employee.objects.filter(department=input_department)
        if input_department is not None:
            department_detail_serializer = DepartmentSerializer(department, many=True)
            return Response(department_detail_serializer.data)
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


# THIS API WILL GIVE NAME OF ALL THE EC2 PRESENT

class EC2InstanceView(APIView):
    ec2_client = boto3.client(
        'ec2',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    def post(self,request):
        ec2 = self.ec2_client.describe_instances()
        ec2_description = request.data.get('description')
        instances=[]
        instances_with_description =[]
        instance_name = ""
        for reservation in ec2['Reservations']:
            for instance_data in reservation['Instances']:
                if 'Tags' in instance_data:
                    for tag in instance_data['Tags']:
                        if tag['Key'] == 'Name':
                                instance_name = tag['Value']
                                break
            Instance_id=instance_data['InstanceId']
            instances_with_description.append({
                "Instance-name": instance_name,
                "Instance-id" : Instance_id,
                "Instance-Discription" : ec2
            })
            instances.append({
                "Instance-name": instance_name,
                "Instance-id" : Instance_id,

            })
        if ec2_description is not None:
            return Response(instances_with_description)
        else:
            return Response(instances)


     
