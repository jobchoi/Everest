# Django가 'models.py' 대신 이 파일들을 보도록 '연결'합니다.

# 1. 'base.py' (2개)
from .base import School_Master, Student_Master

# 2. 'masters.py' (3개 - Department_Master 추가)
from .masters import Teacher_Master, Category_Master, Department_Master

# 3. 'records.py' (3개 - Activity_Log, Goal_History 추가)
from .records import Grade_Sheet, Activity_Log, Goal_History