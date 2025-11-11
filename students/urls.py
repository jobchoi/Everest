from django.urls import path
from . import views  # 'views.py' 파일을 import

urlpatterns = [
    # 'http://.../students/list/' 주소와 'views.py'의 함수를 '연결'
    path('list/', views.student_list_view, name='student_list'),

    # 2. [추가] '학생 상세' (화면 2)
    #    'http://.../students/detail/<uuid:student_id>/' 라는 주소로 접속하면,
    #    '주소'에 포함된 'student_id' 값을 'views.py'의 함수로 '전달'.
    path('detail/<uuid:student_id>/', views.student_detail_view, name='student_detail'),

    # 3. [추가] 'AI(B-an)' 태그 추출을 위한 'API' 엔드포인트
    #    (JavaScript가 'POST' 요청을 '보낼' 주소)
    path('api/extract-tags/', views.api_extract_tags_view, name='api_extract_tags'),
]