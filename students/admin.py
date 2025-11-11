# [H-162] 'students/admin.py'

from django.contrib import admin

# 1. [추가] '항해일지 111번'의 'models/__init__.py'에 정의된
#    '8개'의 '모든' 모델을 'import' 합니다.
from .models import (
    School_Master, 
    Student_Master, 
    Teacher_Master, 
    Category_Master, 
    Department_Master, 
    Grade_Sheet, 
    Activity_Log, 
    Goal_History
)

# 2. [추가] 'import'한 '8개' 모델을 'admin 사이트'에 '등록(register)'합니다.
#    (이 코드가 있어야 '관리자 페이지'에서 '데이터'를 '추가/수정'할 수 있습니다.)
admin.site.register(School_Master)
admin.site.register(Student_Master)
admin.site.register(Teacher_Master)
admin.site.register(Category_Master)
admin.site.register(Department_Master)
admin.site.register(Grade_Sheet)
admin.site.register(Activity_Log)
admin.site.register(Goal_History)