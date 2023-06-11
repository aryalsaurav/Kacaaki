from rest_framework import serializers
from .models import NepaliClass, DanceClass
from users.models import User, NepaliStudent, DanceStudent, Teacher


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
        

    