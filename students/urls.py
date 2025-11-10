from django.urls import path
from . import views  # 'views.py' 파일을 import

urlpatterns = [
    # 'http://.../students/list/' 주소와 'views.py'의 함수를 '연결'
    path('/students/list/', views.student_list_view, name='student_list'),
]