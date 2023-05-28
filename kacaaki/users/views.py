from django.shortcuts import render
from rest_framework.response import Response
from .serializers import  (
    UserLoginSerializer,
    AdminUserSerializer,
    UserUpdateSerializer,
    NepaliStudentSerializer,
    NepaliStudentUpdateSerializer,
    DanceStudentSerializer,
    DanceStudentUpdateSerializer,
    TeacherSerializer,
    TeacherUpdateSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    UserEmailSerializer,

)
from rest_framework.views import  APIView
from rest_framework.parsers import  JSONParser
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from .models import  (
    User,
    NepaliStudent,
    DanceStudent,
    Teacher,
    Token,
   
)
from rest_framework import viewsets
from rest_framework import  generics
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import  permissions
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import login
from .utils import verify_token,user_password_reset_email

# from rest_framework.authtoken.models import Token



# Create your views here.
class AdminUserView(APIView):

    def get(self,request):
        queryset = User.objects.filter(is_staff=True)
        serializer = AdminUserSerializer(queryset,many=True)
        context = {
            "status":200,
            "message":"All User got successfully",
            "data":serializer.data
        }
        return Response(context,status=200)
 
    def post(self, request,*args,**kwargs):
        serializer = AdminUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                "status":201,
                "message":"User created successfully",
                "data":serializer.data

            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                'status':400,
                "message":"Entered data is not valid",
                "error":serializer.errors
            }
            return Response(context,status=400)

class AdminUserDPDView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    
    def get(self,request,pk):
        user = self.get_object(pk)
        serializer = AdminUserSerializer(user)
        context = {
            "status":200,
            "message":f"User {pk} got successfully",
            "data":serializer.data
        }
        return Response(context,status=200)

    def put(self,request,pk):
        user = self.get_object(pk)
        if request.user != user:
            context = {
                "status":403,
                "message":"You do not have permission to update this user"
            }
            return Response(context,status=403)
        serializer = UserUpdateSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                "status":200,
                "message":f"User {pk} data updated successfully",
                "data":serializer.data
            }
            return Response(context,status=200)
        else:
            context = {
                "status":400,
                "message":"Entered data is not valided",
                "error":serializer.errors
            }
            return Response(context,status=400)
    
    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        context = {
            "status":200,
            "message":"User deleted successfully"
        }
        return Response(context,status=200)



#Nepali Student View
class NepaliStudentView(APIView):
    def get(self,request):
        queryset = NepaliStudent.objects.all()
        serializer = NepaliStudentSerializer(queryset,many=True)
        context = {
            "status":200,
            "message":"All Nepali Student got successfully",
            "data":serializer.data
        }
        return Response(context,status=200)
 
    def post(self, request,*args,**kwargs):
        serializer = NepaliStudentSerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer)
            serializer.save()
            context = {
                "status":201,
                "message":"Nepali Student created successfully",
                "data":serializer.data

            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                'status':400,
                "message":"Entered data is not valid",
                "error":serializer.errors
            }
            return Response(context,status=400)



class NepaliStudentDPDView(APIView):
    def get_object(self,pk):
        try:
            return NepaliStudent.objects.get(pk=pk)
        except NepaliStudent.DoesNotExist:
            raise Http404
    
    def get(self,request,pk):
        nepali_student = self.get_object(pk)
        
        if request.user.is_staff is True or request.user == nepali_student.user:
            serializer = NepaliStudentSerializer(nepali_student)
            context = {
                "status":200,
                "message":f"Nepali Student {pk} got successfully",
                "data":serializer.data
            }
            return Response(context,status=200)
        else:
            
            context = {
                "status":403,
                "message":"You do not have permission to view this student"
            }
            return Response(context,status=403)

    def put(self,request,pk):
        nepali_student = self.get_object(pk)
        if request.user != nepali_student.user:
            context = {
                "status":403,
                "message":"You do not have permission to update this student"
            }
            return Response(context,status=403)
        user_serializer = UserUpdateSerializer(nepali_student.user,data=request.data,partial=True)
        nepali_student_serializer = NepaliStudentUpdateSerializer(nepali_student,data=request.data,partial=True)
        if user_serializer.is_valid() and nepali_student_serializer.is_valid():
            user_serializer.save()
            nepali_student_serializer.save()
            context = {
                "status":200,
                "message":"Nepali Student data updated successfully",
                "data": {
                    "user":user_serializer.data,
                    "nepali_student":nepali_student_serializer.data
                }
            }
            return Response(context,status=200)
        else:
            context = {
                "status":400,
                "message":"Entered data is not valided",
                "error":{
                    "user":user_serializer.errors,
                    "nepali_student":nepali_student_serializer.errors
                }
            }
            return Response(context,status=400)
    
    def delete(self,request,pk):
        nepali_student = self.get_object(pk)
        if request.user != nepali_student.user:
            context = {
                "status":403,
                "message":"You do not have permission to delete this student"
            }
            return Response(context,status=403)
        nepali_student.delete()
        context = {
            "status":200,
            "message":"Nepali Student deleted successfully"
        }
        return Response(context,status=200)


#Dance Student View

class DanceStudentView(APIView):
    def get(self,request):
        queryset = DanceStudent.objects.all()
        serializer = DanceStudentSerializer(queryset,many=True)
        context = {
            "status":200,
            "message":"All Dance Student got successfully",
            "data":serializer.data
        }
        return Response(context,status=200)
 
    def post(self, request,*args,**kwargs):
        serializer = DanceStudentSerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer)
            serializer.save()
            context = {
                "status":201,
                "message":"Dance Student created successfully",
                "data":serializer.data

            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                'status':400,
                "message":"Entered data is not valid",
                "error":serializer.errors
            }
            return Response(context,status=400)


class DanceStudentDPDView(APIView):
    def get_object(self,pk):
        try:
            return DanceStudent.objects.get(pk=pk)
        except DanceStudent.DoesNotExist:
            raise Http404
        
    
    def get(self,request,pk):
        dance_student = self.get_object(pk)
        if request.user.is_staff is True or request.user == dance_student.user:
            serializer = DanceStudentSerializer(dance_student)
            context = {
                "status":200,
                "message":f"Dance Student {pk} got successfully",
                "data":serializer.data
            }
            return Response(context,status=200)
        else:
            context = {
                "status":403,
                "message":"You do not have permission to view this student"
            }
            return Response(context,status=403)

    def put(self,request,pk):
        dance_student = self.get_object(pk)
        if request.user != dance_student.user:
            context = {
                "status":403,
                "message":"You do not have permission to update this student"
            }
            return Response(context,status=403)
        user_serializer = UserUpdateSerializer(dance_student.user,data=request.data,partial=True)
        dance_student_serializer = DanceStudentUpdateSerializer(dance_student,data=request.data,partial=True)
        if user_serializer.is_valid() and dance_student_serializer.is_valid():
            user_serializer.save()
            dance_student_serializer.save()
            context = {
                "status":200,
                "message":f"Dance student {pk} data updated successfully",
                "data": {
                    "user":user_serializer.data,
                    "dance_student":dance_student_serializer.data
                }
            }
            return Response(context,status=200)
        else:
            context = {
                "status":400,
                "message":"Entered data is not valided",
                "error":{
                    "user":user_serializer.errors,
                    "dance_student":dance_student_serializer.errors
                }
            }
            return Response(context,status=400)
    
    def delete(self,request,pk):
        dance_student = self.get_object(pk)
        if request.user != dance_student.user:
            context = {
                "status":403,
                "message":"You do not have permission to delete this student"
            }
            return Response(context,status=403)
        dance_student.delete()
        context = {
            "status":200,
            "message":"Dance Student deleted successfully"
        }
        return Response(context,status=200)

#Teacher View

class TeacherView(APIView):
    def get(self,request):
        queryset = Teacher.objects.all()
        serializer = TeacherSerializer(queryset,many=True)
        context = {
            "status":200,
            "message":"All Teacher got successfully",
            "data":serializer.data
        }
        return Response(context,status=200)
 
    def post(self, request,*args,**kwargs):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer)
            serializer.save()
            context = {
                "status":201,
                "message":"Teacher created successfully",
                "data":serializer.data

            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                'status':400,
                "message":"Entered data is not valid",
                "error":serializer.errors
            }
            return Response(context,status=400)


class TeacherDPDView(APIView):
    def get_object(self,pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404
        
    
    def get(self,request,pk):
        teacher = self.get_object(pk)
        if request.user == teacher.user or request.user.is_staff is True:
            serializer = TeacherSerializer(teacher)
            context = {
                "status":200,
                "message":f"Teacher {pk} got successfully",
                "data":serializer.data
            }
            return Response(context,status=200)
        else:
            context = {
                "status":403,
                "message":"You do not have permission to view this teacher"
            }
            return Response(context,status=403)

    def put(self,request,pk):
        teacher = self.get_object(pk)
        if request.user != teacher.user:
            context = {
                "status":403,
                "message":"You do not have permission to update this teacher"
            }
            return Response(context,status=403)
        user_serializer = UserUpdateSerializer(teacher.user,data=request.data,partial=True)
        teacher_serializer = TeacherUpdateSerializer(teacher,data=request.data,partial=True)
        if user_serializer.is_valid() and teacher_serializer.is_valid():
            user_serializer.save()
            teacher_serializer.save()
            context = {
                "status":200,
                "message":f"Teacher {pk} data updated successfully",
                "data": {
                    "user":user_serializer.data,
                    "teacher":teacher_serializer.data
                }
            }
            return Response(context,status=200)
        else:
            context = {
                "status":400,
                "message":"Entered data is not valided",
                "error":{
                    "user":user_serializer.errors,
                    "teacher":teacher_serializer.errors
                }
            }
            return Response(context,status=400)
    
    def delete(self,request,pk):
        teacher = self.get_object(pk)
        if request.user != teacher.user:
            context = {
                "status":403,
                "message":"You do not have permission to delete this teacher"
            }
            return Response(context,status=403)
        teacher.delete()
        context = {
            "status":200,
            "message":"Teacher deleted successfully"
        }
        return Response(context,status=200)













class VerifyEmailView(APIView):
    """
    GET auth/verify-email/<str:token>/
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, token, *args, **kwargs):
        user = verify_token(token)
        if user:
            user.is_active = True
            user.save() 
            context = {
                "status":200,
                "message":"Email verified successfully"
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "status":400,
                "message":"Invalid token"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetEmail(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserEmailSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = User.objects.get(email=email)
            user_password_reset_email(user)
            context = {
                "status":200,
                "message":"Password reset email sent successfully"
            }
            return Response(context,status=200)
        else:
            context = {
                'status':400,
                'message':'failed',
                'error':serializer.errors
            }
            return Response(context,status=400)
            

class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = serializer.validated_data['user']
            token,created = Token.objects.get_or_create(user=user)
           
            response = {
                'success': 200,
                'message': 'User logged in  successfully',
                'user': email,
                'token': token.key,
                
                }
            status_code = status.HTTP_200_OK

            return Response(response, status=status_code)
        else:
            context = {
                'status':400,
                'message':'failed',
                'error':serializer.errors
            }
            return Response(context,status=400)


        
class LogoutView(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        context = {
            'status':200,
            'message':'User logged out successfully',
        }
        return Response(context,status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

   

    def put(self,request,*args,**kwargs):
        user  = request.user
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                context = {
                    'status':400,
                    'message':'failed',
                    'error':'Old password did not match'
                }
                return Response(context,status=400)
            elif user.check_password(serializer.data.get("new_password2")):
                context ={
                    'status':400,
                    'message':'failed',
                    'error':'Old password cannot be new password'
                }
                return Response(context,status=400)
            
           
            
            elif (serializer.data.get('new_password1')!=serializer.data.get('new_password2')):
                context = {
                    'status':400,
                    'message':'failed',
                    'error':'Password did not match'
                }
                return Response(context,status=400)
            else:

                user.set_password(serializer.data.get('new_password2'))
                user.save()
                context = {
                    'status':200,
                    'message':'Password changed successfully'
                }
                return Response(context,status=200)
        else:
            context = {
                'status':400,
                'message':'failed',
                'errors':serializer.errors
            }
            return Response(context,status=400)
        
    