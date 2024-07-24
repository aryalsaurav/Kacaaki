from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..models import (
    User,
    NepaliStudent,
    DanceStudent,
    Teacher,
    ClassTime,
    VideoUpload
)
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from ..utils import user_verification_email
from datetime import datetime
import redis 
import pickle





times = [t[1] for t in ClassTime.choices]
def validate_class_time(value):
    for v in value:
        if v not in times:
            raise serializers.ValidationError(
               "Class time entered is not valid"
                
            )



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','password','full_name','gender','age','phone','photo','city','state','country','user_type','is_staff','is_superuser','is_active','created_at']
        extra_kwargs = {
            'password':{'write_only':True}
        }
        # fields = "__all__"
    

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','password','full_name','gender','age','phone','photo','city','state','country','is_staff','is_superuser','is_active','created_at']
        extra_kwargs = {
            'password':{'write_only':True},
            'is_staff':{'default':True},
            
        }
        # fields = "__all__"
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(password=make_password(password),**validated_data)
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','full_name','gender','age','phone','photo','city','state','country','is_staff','is_superuser','is_active','created_at']
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
            'is_staff':{'required':False},
            'is_superuser':{'required':False},
            'is_active':{'required':False},
            
        }
    
    def update(self,instance,validated_data):
        instance.email = validated_data.get('email',instance.email)
        instance.full_name = validated_data.get('full_name',instance.full_name)
        instance.gender = validated_data.get("gender",instance.gender)
        instance.age = validated_data.get('age',instance.age)
        instance.phone = validated_data.get('phone',instance.phone)
        instance.photo = validated_data.get('photo',instance.photo)
        instance.city = validated_data.get('city',instance.city)
        instance.state = validated_data.get('state',instance.state)
        instance.country = validated_data.get('country',instance.country)
        instance.is_staff = validated_data.get('is_staff',instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser',instance.is_superuser)
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.save()
        return instance

    
        
class NepaliStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class_time = serializers.ListField(validators=[validate_class_time])
    class Meta:
        model = NepaliStudent
        fields = fields = ['id','user','signing_for','parents_name','nepali_at_home','listening','speaking','reading','writing','course_level','session_type','class_time','goal_for_class','hear_from','special_request','other_classes']
        

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_password = user_data.pop('password')
        user = User.objects.create(password=make_password(user_password),**user_data)
        user.is_active=False
        user.save()
        nepali_student = NepaliStudent.objects.create(user=user,**validated_data)
        user_verification_email(user)
        return nepali_student




class NepaliStudentUpdateSerializer(serializers.ModelSerializer):
    class_time = serializers.ListField(validators=[validate_class_time])
    class Meta:
        model = NepaliStudent
        fields = fields = ['id','signing_for','parents_name','nepali_at_home','listening','speaking','reading','writing','course_level','session_type','class_time','goal_for_class','hear_from','special_request','other_classes']
        
    
    def update(self,instance,validated_data):
        instance.signing_for = validated_data.get('signing_for',instance.signing_for)
        instance.parents_name = validated_data.get('parents_name',instance.parents_name)
        instance.nepali_at_home = validated_data.get('nepali_at_home',instance.nepali_at_home)
        instance.listening = validated_data.get('listening',instance.listening)
        instance.speaking = validated_data.get('speaking',instance.speaking)
        instance.reading = validated_data.get('reading',instance.reading)
        instance.writing = validated_data.get('writing',instance.writing)
        instance.course_level = validated_data.get('course_level',instance.course_level)
        instance.session_type = validated_data.get('session_type',instance.session_type)
        instance.class_time = validated_data.get('class_time',instance.class_time)
        instance.goal_for_class = validated_data.get('goal_for_class',instance.goal_for_class)
        instance.hear_from = validated_data.get('hear_from',instance.hear_from)
        instance.special_request = validated_data.get('special_request',instance.special_request)
        instance.other_classes = validated_data.get('other_classes',instance.other_classes)
        instance.save()
        return instance



class DanceStudentSerializer(serializers.ModelSerializer):
    class_time = serializers.ListField(validators=[validate_class_time])
    user = UserSerializer()
    class Meta:
        model = DanceStudent
        fields = ['id','user','signing_for','parents_name','dance_skills','dance_style','session_type','class_time','goal_for_class','hear_from','special_request','other_classes']
        

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_password = user_data.pop('password')
        user = User.objects.create(password=make_password(user_password),**user_data)
        dance_student = DanceStudent.objects.create(user=user,**validated_data)
        return dance_student


class DanceStudentUpdateSerializer(serializers.ModelSerializer):
    class_time = serializers.ListField(validators=[validate_class_time])
    class Meta:
        model = DanceStudent
        fields = ['id','user','signing_for','parents_name','dance_skills','dance_style','session_type','class_time','goal_for_class','hear_from','special_request','other_classes']
        
    
    def update(self,instance,validated_data):
        instance.signing_for = validated_data.get('signing_for',instance.signing_for)
        instance.parents_name = validated_data.get('parents_name',instance.parents_name)
        instance.dance_skills = validated_data.get('dance_skills',instance.dance_skills)
        instance.dance_style = validated_data.get('dance_style',instance.dance_style)
        instance.session_type = validated_data.get('session_type',instance.session_type)
        instance.class_time = validated_data.get('class_time',instance.class_time)
        instance.goal_for_class = validated_data.get('goal_for_class',instance.goal_for_class)
        instance.hear_from = validated_data.get('hear_from',instance.hear_from)
        instance.special_request = validated_data.get('special_request',instance.special_request)
        instance.other_classes = validated_data.get('other_classes',instance.other_classes)
        instance.save()
        return instance


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Teacher
        fields = ['id','user','teacher_type','zoom_link']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_password = user_data.pop('password')
        user = User.objects.create(password=make_password(user_password),**user_data)
        teacher = Teacher.objects.create(user=user,**validated_data)
        return teacher
    

class TeacherUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id','teacher_type','zoom_link']
    
    def update(self,instance,validated_data):
        instance.teacher_type = validated_data.get('teacher_type',instance.teacher_type)
        instance.zoom_link = validated_data.get('zoom_link',instance.zoom_link)
        instance.save()
        return instance




class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = ['video','adminVideo','clientVideo']
    
    
    
    def create(self, validated_data):
        video = VideoUpload.objects.create(**validated_data)
        return video










class PasswordChangeSerializer(serializers.Serializer):
    
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate_new_password1(self, value):
        try:
            password_validation.validate_password(value)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return value

class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
   

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
            user_filter = User.objects.filter(email=email)
            if user_filter.exists():
                raise serializers.ValidationError(
                    "Invalid password"
                )
                
            else:
                raise serializers.ValidationError(
                    "User with this email address doesn't exists. Please register first."
                )

        if not user.is_active:
            user_verification_email(user)
            raise serializers.ValidationError(
                'Please verify your email to login. We have just sent you verification email.'
            
            )
        user.last_login = datetime.now()
        user.save()

        validated_data['user'] = user
        
        return validated_data
    
    

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')