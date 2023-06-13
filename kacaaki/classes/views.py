from django.shortcuts import render
from django.http import HttpResponse,Http404
from .models import NepaliClass, DanceClass, Assignment, AssignmentSubmission, AssignmentFile
from .serializers import (
    NepaliClassSerializer,
    DanceClassSerializer,
    AssignmentSerializer,
    AssignmentSubmissionSerializer,
    AssignmentFileSerializer,
    AssignmentSubmissionDetailSerializer,
    AssignmentFileUploadSerializer,

)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import django_filters
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from users.models import User, NepaliStudent, DanceStudent, Teacher


# Create your views here.


#Nepali Class Views


class NepaliClassView(APIView):
    def get(self, request):
        nepali_classes = NepaliClass.objects.all()
        serializer = NepaliClassSerializer(nepali_classes, many=True)
        context = {
            'status':200,
            'nepali_classes': serializer.data,
        }
        return Response(context,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NepaliClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'status':201,
                'message': 'Nepali Class created successfully',
                'nepali_class': serializer.data,
            }
            return Response(context, status=status.HTTP_201_CREATED)

        else:
            context = {
                'status':400,
                'message': 'Nepali Class not created',
                'errors': serializer.errors,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)



class NepaliClassDetailView(APIView):
    def get_object(self, pk):
        try:
            return NepaliClass.objects.get(pk=pk)
        except NepaliClass.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        nepali_class = self.get_object(pk)
        serializer = NepaliClassSerializer(nepali_class)
        context = {
            'status':200,
            'nepali_class': serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)

    def put(self, request, pk):
        nepali_class = self.get_object(pk)
        serializer = NepaliClassSerializer(nepali_class, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                'status':200,
                'message': 'Nepali Class updated successfully',
                'nepali_class': serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)

        else:
            context = {
                'status':400,
                'message': 'Nepali Class not updated',
                'errors': serializer.errors,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        nepali_class = self.get_object(pk)
        nepali_class.delete()
        context = {
            'status':200,
            'message': 'Nepali Class deleted successfully',
        }
        return Response(context, status=status.HTTP_200_OK)


class NepaliclassFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = NepaliClass
        fields = ['name', 'teacher', 'students']


















#Dance Class Views

class DanceClassView(APIView):
    def get(self, request):
        dance_classes = DanceClass.objects.all()
        serializer = DanceClassSerializer(dance_classes, many=True)
        context = {
            'status':200,
            'dance_classes': serializer.data,
        }
        return Response(context,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DanceClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'status':201,
                'message': 'Dance Class created successfully',
                'dance_class': serializer.data,
            }
            return Response(context, status=status.HTTP_201_CREATED)

        else:
            context = {
                'status':400,
                'message': 'Dance Class not created',
                'errors': serializer.errors,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)



class DanceClassDetailView(APIView):
    def get_object(self,pk):
        try:
            return DanceClass.objects.get(pk=pk)
        except DanceClass.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        dance_class = self.get_object(pk)
        serializer = DanceClassSerializer(dance_class)
        context = {
            'status':200,
            'dance_class': serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)


    def put(self, request, pk):
        dance_class = self.get_object(pk)
        serializer = DanceClassSerializer(dance_class, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                'status':200,
                'message': 'Dance Class updated successfully',
                'dance_class': serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)

        else:
            context = {
                'status':400,
                'message': 'Dance Class not updated',
                'errors': serializer.errors,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        dance_class = self.get_object(pk)
        dance_class.delete()
        context = {
            'status':200,
            'message': 'Dance Class deleted successfully',
        }
        return Response(context, status=status.HTTP_200_OK)




#assignment view

class AssignmentView(APIView):
    def get(self,request):
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        context = {
            'status':200,
            'assignments': serializer.data,
        }
        return Response(context,status=status.HTTP_200_OK)


    def post(self, request):
        serializer = AssignmentSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context = {
                'status':201,
                'message': 'Assignment created successfully',
                'assignment': serializer.data,
            }
            return Response(context, status=status.HTTP_201_CREATED)

        else:
            context = {
                'status':400,
                'message': 'Assignment not created',
                'errors': serializer.errors,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)



class AssignmentDetailView(APIView):
    def get_object(self,pk):
        try:
            return Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        assignment = self.get_object(pk)
        serializer = AssignmentSerializer(assignment)
        context = {
            'status':200,
            'assignment': serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)


    def put(self, request, pk):
        assignment = self.get_object(pk)
        serializer = AssignmentSerializer(assignment, data=request.data, partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context = {
                'status':200,
                'message': 'Assignment updated successfully',
                'assignment': serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)

        else:
            context = {
                'status':400,
                'message': 'Assignment not updated',
                'errors': serializer.errors,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        assignment = self.get_object(pk)
        assignment.delete()
        context = {
            'status':200,
            'message': 'Assignment deleted successfully',
        }
        return Response(context, status=status.HTTP_200_OK)










class AssignmentSubmissionView(APIView):
    # parser_classes = (MultiPartParser, FormParser)
    def get(self,request):
        assignment_submissions = AssignmentSubmission.objects.all()
        serializer = AssignmentSubmissionDetailSerializer(assignment_submissions, many=True)
        print(serializer.data)
        context = {
            'status':200,
            'data': serializer.data,
        }
        return Response(context,status=status.HTTP_200_OK)

    def post(self,request):
        # print(request.data)
        serializer = AssignmentSubmissionSerializer(data=request.data,context = {'request': request})
        files = request.FILES.getlist('a_file')
        
        if serializer.is_valid():
            
            serializer.save()
            assignment_submission = AssignmentSubmission.objects.get(pk=serializer.data['id'])
            for file in files:
                AssignmentFile.objects.create(assignment_submission=assignment_submission, a_file=file)
            context = {
                'status':201,
                'message': 'Assignment submitted successfully',
                'assignment_submission': serializer.data,
            }
            return Response(context, status=status.HTTP_201_CREATED)

        else:
            context = {
                'status':400,
                'message': 'Assignment not submitted',
                'errors': serializer.errors,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)



class AssignmentSubmissionDetailView(APIView):
    # parser_classes = (MultiPartParser, FormParser)
    def get_object(self,pk):
        try:
            return AssignmentSubmission.objects.get(pk=pk)
        except AssignmentSubmission.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        assignment_submission = self.get_object(pk)
        serializer = AssignmentSubmissionDetailSerializer(assignment_submission)
        context = {
            'status':200,
            'assignment_submission': serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)
    

    def post(self, request, pk):
        assignment_submission = self.get_object(pk)
        if not assignment_submission.assignment.nepali_class.students.filter(user=request.user).exists():
            context = {
                'status':400,
                'message': 'You are not the student of this class',
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        serializer = AssignmentFileUploadSerializer(data=request.data,many=True)
        files = request.FILES.getlist('a_file')
        if serializer.is_valid():
            serializer.save()
            li = []
            for file in range(len(files)):
                a = AssignmentFile.objects.create(assignment_submission=assignment_submission,a_file=files[file])
                li.append(files[file].name)
            

            
            context = {
                'status':201,
                'message': 'Assignment submitted successfully',
                'assignment_submission': li
            }
            return Response(context, status=status.HTTP_201_CREATED)

        else:
            context = {
                'status':400,
                'message': 'Assignment not submitted',
                'errors': serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)






    def delete(self, request, pk):
        assignment_submission = self.get_object(pk)
        assignment_submission.delete()
        context = {
            'status':200,
            'message': 'Assignment deleted successfully',
        }
        return Response(context, status=status.HTTP_200_OK)


    