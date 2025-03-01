from django.contrib import admin

# Register your models here.
from .models import Employee,User

admin.site.register(Employee)
admin.site.register(User)
