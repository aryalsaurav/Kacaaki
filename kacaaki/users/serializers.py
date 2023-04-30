from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (
    User,
    NepaliStudent,
    DanceStudent,
    Teacher,
    ManagementStaff,
)
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','password','full_name','gender','age','phone','photo','city','state','country']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    

    
        
class NepaliStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = NepaliStudent
        fields = fields = ['id','user','signing_for','parents_name','nepali_at_home','listening','speaking','reading','writing','course_level','session_type','class_time','goal_for_class','hear_from','special_request','other_classes']
        

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_password = user_data.pop('password')
        user = User.objects.create(password=make_password(user_password),**user_data)
        nepali_student = NepaliStudent.objects.create(user=user,**validated_data)
        return nepali_student

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','full_name','gender','age','phone','photo','city','state','country']
        extra_kwargs = {
            'email':{'required':False},
            'full_name':{'required':False},
            'gender':{'required':False},
            'age':{'required':False},
            'phone':{'required':False},
            'photo':{'required':False},
            'city':{'required':False},
            'state':{'required':False},
            'country':{'required':False},
        }

class NepaliStudentUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()
    class Meta:
        model = NepaliStudent
        fields = fields = ['id','user','signing_for','parents_name','nepali_at_home','listening','speaking','reading','writing','course_level','session_type','class_time','goal_for_class','hear_from','special_request','other_classes']
        
    
    def update(self,instance,validated_data):
        print(validated_data)
        print("hello")
        user_data = validated_data.pop('user',None)
        print(user_data)
        user_serializer = UserUpdateSerializer(instance.user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            raise serializers.ValidationError(user_serializer.errors)
        instance = super().update(instance, validated_data)
        return instance







class PasswordChangeSerializer(serializers.Serializer):
    
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
   

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self,validated_data):
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
       
        user = authenticate(email=email, password=password)
       
        if user is None:
            raise serializers.ValidationError(
                'A user wi.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        validated_data['user'] = user
        
        return validated_data