from rest_framework import serializers
from .models import User,Employee




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password','mobile')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            mobile=validated_data['mobile'])
        return user


class LoginSerializer(serializers.Serializer):
    
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True, write_only= True)
    
class DesignationSerializer(serializers.ModelSerializer):
    username= serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Employee
        fields = ['id','username','designation']

class DepartmentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Employee
        fields = ['id','username','department']
