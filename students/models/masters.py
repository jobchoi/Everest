
from django.db import models
import uuid
from .base import School_Master  #   (Table 2 참조)

# -----------------------------------------------------------------
# [2. (복사/붙여넣기)]   (Table 3: Teacher_Master)
# -----------------------------------------------------------------
class Teacher_Master(models.Model):
    teacher_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    #   (보안 1원칙 - '참조' 방식)
    school_id = models.ForeignKey(School_Master, on_delete=models.PROTECT)
    
    teacher_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.teacher_name} ({self.school_id.school_name})"

# -----------------------------------------------------------------
# [3. (복사/붙여넣기)] (Table 6: Category_Master)
# -----------------------------------------------------------------
class Category_Master(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # (GIGO 방지용 '표준화' 필드)
    category_name = models.CharField(max_length=100, unique=True) # (예: '교과', '창체', '봉사')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name
    
class Department_Master(models.Model):
    dept_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # (GIGO 방지용 '표준화' 필드)
    dept_name = models.CharField(max_length=100, unique=True) # (예: '컴퓨터공학과')
    dept_keywords = models.JSONField(default=dict, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dept_name