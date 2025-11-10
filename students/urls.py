from django.urls import path
from . import views  # 1. '항해일지 134번'의 'views.py' 파일을 import

urlpatterns = [
    # 2. 'http://.../students/list/' 라는 주소로 '접속'하면,
    #    'views.py'의 'student_list_view' 함수를 '실행'하라는 의미입니다.
    path('list/', views.student_list_view, name='student_list'),
]