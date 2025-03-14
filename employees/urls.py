from django.urls import path
from .views import EmployeeViews
from .views import RegisterViews,LoginViews,DepartmentViews,DesignationViews,S3BucketView,EC2InstanceView


urlpatterns = [
    path('employees/', EmployeeViews.as_view(), name='employee-detail'),
    path('Register/', RegisterViews.as_view(), name='Register-detail'),
    path('Login/', LoginViews.as_view(), name='Login-detail'),
    path('Department/', DepartmentViews.as_view(), name='Department-detail'),
    path('Designation/', DesignationViews.as_view(), name='Designation-detail'),
    path('Get_S3/', S3BucketView.as_view(),name='S3-Bucket-detail'),
    path('Get_ec2/', EC2InstanceView.as_view(),name='EC2-Instance-detail')
]

