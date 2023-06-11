from django.shortcuts import render
from django.http import HttpResponse,Http404
from .models import NepaliClass, DanceClass
from .serializers import (
    NepaliClassSerializer,
    DanceClassSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

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