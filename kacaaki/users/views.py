from django.shortcuts import render
from rest_framework.response import Response
from .serializers import  (
    UserSerializer,
    NepaliStudentSerializer,
    PasswordChangeSerializer,
    UserLoginSerializer,
    NepaliStudentSerializer,
    NepaliStudentUpdateSerializer


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
    ManagementStaff,
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
from django.http import HttpResponseRedirect
from django.contrib.auth import login
# from rest_framework.authtoken.models import Token



# Create your views here.

class UserDeleteView(APIView):
    def delete(self,request):
        try:
            user = request.user
            user.delete()
            context = {
                "status":200,
                "message":"User deleted successfully"
            }
            return Response(context,status=200)
        except:
            context = {
                "status":400,
                "message":"User does not exist"
            }
            return Response(context,status=400)


class NepaliStudentView(APIView):
    def get(self,request):
        queryset = NepaliStudent.objects.all()
        serializer = NepaliStudentSerializer(queryset,many=True)
        context = {
            "status":200,
            "message":"All Nepali Student got successfully",
            "user":serializer.data
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
                "user":serializer.data

            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                'status':400,
                "message":"Entered data is not valid",
                "error":serializer.errors
            }
            return Response(context,status=400)




class StudentUpdateView(generics.UpdateAPIView):
    queryset = NepaliStudent.objects.all()
    serializer_class = NepaliStudentUpdateSerializer
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        user = request.user # get the current user
        student = self.get_object()
        if student.user != user:
            return Response({'message': 'You do not have permission to update this student'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class NepaliStudentDPDView(APIView):
    def get_object(self,pk):
        try:
            return NepaliStudent.objects.get(pk=pk)
        except NepaliStudent.DoesNotExist:
            raise Http404
    
    def get(self,request,pk):
        nepali_student = self.get_object(pk)
        serializer = NepaliStudentUpdateSerializer(nepali_student)
        context = {
            "status":200,
            "message":f"Nepali Student {pk} got successfully",
            "user":serializer.data
        }
        return Response(context,status=200)

    def put(self,request,pk):
        nepali_student = self.get_object(pk)
        if request.user != nepali_student.user:
            context = {
                "status":403,
                "message":"You do not have permission to update this student"
            }
            return Response(context,status=403)
        serializer = NepaliStudentUpdateSerializer(nepali_student,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                "status":200,
                "message":f"Nepali Student {pk} updated successfully",
                "user":serializer.data
            }
            return Response(context,status=200)
        else:
            context = {
                "status":400,
                "message":"Entered data is not valided",
                "error":serializer.errors
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
            token = Token.objects.create(user=user)
           
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


@method_decorator(login_required,name='dispatch')
class PasswordChangeView(APIView):
    def put(self,request):
        user = request.user
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
                    'message':'success'
                }
                return Response(context,status=200)
        else:
            context = {
                'status':400,
                'message':'failed',
                'errors':serializer.errors
            }
            return Response(context,status=400)
