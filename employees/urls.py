from django.urls import path
# from .views import EmployeeViews
from .views import RegisterViews,LoginViews


urlpatterns = [
    # path('employees/', EmployeeViews.as_view(), name='employee-detail'),
    path('Register/', RegisterViews.as_view(), name='Register-detail'),
    path('Login/', LoginViews.as_view(), name='Login-detail'),
]

