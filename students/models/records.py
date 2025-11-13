# [1.] /home/lin/study/web/django/students/models/records.py
from django.db import models
import uuid
from .base import Student_Master  #    (Table 1 참조)

from .masters import Teacher_Master, Category_Master, Department_Master

# -----------------------------------------------------------------
# [2. (복사/붙여넣기)]    (Table 5: Grade_Sheet)
# -----------------------------------------------------------------
class Grade_Sheet(models.Model):
    grade_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    #    (학생 '참조')
    student_uuid = models.ForeignKey(Student_Master, on_delete=models.CASCADE)

    semester = models.CharField(max_length=50) # (예: '1-1', '1-2')
    subject_name = models.CharField(max_length=100) # (예: '수학')
    
    #    (AI 분석용 '피처 엔지니어링')
    raw_score = models.FloatField(null=True, blank=True) # 원점수
    grade_rank = models.IntegerField(null=True, blank=True) # 등급
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        #    (GIGO 방지: 학생 1명은 '1-1 수학' 성적을 1개만 갖는다)
        unique_together = ('student_uuid', 'semester', 'subject_name')

    def __str__(self):
        return f"{self.student_uuid.student_name} - {self.semester} {self.subject_name}"
    
class Activity_Log(models.Model):
    activity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    #    (GIGO 방지용 '참조')
    student_uuid = models.ForeignKey(Student_Master, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher_Master, on_delete=models.SET_NULL, null=True) # 교사 (삭제되도 기록은 남김)
    category_id = models.ForeignKey(Category_Master, on_delete=models.PROTECT) # 구분 (필수)

    activity_date = models.DateField() # 활동 일자
    
    # (B안 워크플로우 - 원본 텍스트)
    content_text = models.TextField() # '교사가 입력한 원본'
    
    #    (AI 분석 결과)
    activity_tags = models.JSONField(default=list) # (예: ['#리더십', '#알고리즘'])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_uuid.student_name} - {self.activity_date}"

# -----------------------------------------------------------------
# [3. (아래에 '추가')] (Table 7: Goal_History)
# -----------------------------------------------------------------
class Goal_History(models.Model):
    goal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student_uuid = models.ForeignKey(Student_Master, on_delete=models.CASCADE)
    
    #  (GIGO 방지용 '참조')
    goal_dept_id = models.ForeignKey(Department_Master, on_delete=models.PROTECT, null=True, blank=True) # 희망 전공

    record_date = models.DateField() # 기록 일자
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_uuid.student_name} - {self.goal_dept_id.dept_name}"