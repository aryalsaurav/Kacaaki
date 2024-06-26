from rest_framework import serializers
from ..models import NepaliClass, DanceClass, Assignment, AssignmentSubmission, AssignmentFile
from users.models import User, NepaliStudent, DanceStudent, Teacher
#import integrityerror 
from django.db import IntegrityError


class NepaliClassSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(queryset=NepaliStudent.objects.all(), many=True)
    class Meta:
        model = NepaliClass
        fields = '__all__'

    def validate_students(self, value):
        if len(value) > 4:
            raise serializers.ValidationError("Maximum 4 students allowed")
        return value

    def create(self, validated_data):
        students = validated_data.pop('students')
        nepali_class = NepaliClass.objects.create(**validated_data)
        for student in students:
            nepali_class.students.add(student)
        return nepali_class
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.teacher = validated_data.get('teacher', instance.teacher)
        students_data = validated_data.pop('students', [])
        instance = super().update(instance, validated_data)
        instance.students.set(students_data)
        instance.save()
        return instance



class DanceClassSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(queryset=DanceStudent.objects.all(), many=True)
    class Meta:
        model = DanceClass
        fields = '__all__'

    def validate_students(self, value):
        if len(value) > 4:
            raise serializers.ValidationError("Maximum 4 students allowed")
        return value

    def create(self, validated_data):
        students = validated_data.pop('students')
        dance_class = DanceClass.objects.create(**validated_data)
        for student in students:
            dance_class.students.add(student)
        return dance_class


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.teacher = validated_data.get('teacher', instance.teacher)
        students_data = validated_data.pop('students', [])
        instance = super().update(instance, validated_data)
        instance.students.set(students_data)
        instance.save()
        return instance




class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'



    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    #validate if the teacher is in the nepali class or not

    def validate(self, data):
        teacher = data['nepali_class'].teacher
        print(teacher)
        if teacher.user != self.context['request'].user:
            raise serializers.ValidationError("You are not the teacher of this class")
        return data

    def create(self, validated_data):
        assignment = Assignment.objects.create(**validated_data)
        return assignment


    def update(self, instance, validated_data):
        instance.topic = validated_data.get('topic', instance.topic)
        instance.nepali_class = validated_data.get('nepali_class', instance.nepali_class)
        instance.save()
        return instance



class AssignmentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentFile
        fields = ['id','a_file']


class AssignmentFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentFile
        fields = ['id','assignment_submission','a_file']
        extra_kwargs = {
                'assignment_submission': {'required': False},
            }



    
    




    



class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    images = AssignmentFileSerializer(many=True, required=False)
    class Meta:
        model = AssignmentSubmission
        fields = ['id','assignment', 'student', 'submitted_at','images']
        extra_kwargs = {
            'student': {'read_only': True},
        }
        

    
    def validate(self, data):
        student = self.context['request'].user
        assignment = data['assignment']
        if not assignment.nepali_class.students.filter(user=student).exists():
            
            raise serializers.ValidationError("You are not the student of this class")
        return data
        

    def create(self, validated_data):
        images_data = validated_data.pop('images',[])
        n_student = self.context['request'].user
        student = NepaliStudent.objects.get(user=n_student)
        try:
            assignment_submission = AssignmentSubmission.objects.create(student=student,**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"status":400,"error": "You have already submitted this assignment"})
        return assignment_submission


    
 



class AssignmentSubmissionDetailSerializer(serializers.ModelSerializer):
    images = AssignmentFileSerializer(many=True, source='assignmentfile_set')
    class Meta:
        model = AssignmentSubmission
        fields = ['id','assignment', 'student', 'submitted_at','images']





    
        


        

    