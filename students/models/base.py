from django.db import models

# Create your models here.
import uuid

class School_Master(models.Model):
    school_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_name = models.CharField(max_length=100)
    # (기타 학교 정보... Phase 1에서는 생략)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.school_name
    

class Student_Master(models.Model):
    student_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # (보안 1원칙 - '참조' 방식)
    school_id = models.ForeignKey(School_Master, on_delete=models.PROTECT) 

    student_name = models.CharField(max_length=100)
    
    # (동명이인 구별용 '상수')
    admission_year = models.IntegerField() 
    
    # (동명이인 구별용)
    birthday = models.DateField()
    
    # (학생 분야)
    # student_field = models.CharField(max_length=50)
    student_field = models.CharField(max_length=50, blank=True, null=True)

    # (더미 데이터 격리)
    DATA_STATUS_CHOICES = [
        ('Active', '활성'),
        ('Dummy', '더미'),
    ]
    data_status = models.CharField(max_length=10, choices=DATA_STATUS_CHOICES, default='Active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_name} ({self.admission_year})"