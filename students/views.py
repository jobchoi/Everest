from django.shortcuts import render
from .models import Student_Master  # '학생 모델' import

# Create your views here.
from .models import Student_Master  # 1. '항해일지 97번'의 '학생 모델'을 import

# -----------------------------------------------------------------
# [2. (추가)] '항해일지 134번' (화면 1: 학생 목록 뷰)
# -----------------------------------------------------------------
def student_list_view(request):
    
    # 3. [핵심 H-32] '더미(Dummy)'를 제외한 '활성(Active)' 학생 데이터만 조회합니다.
    #    (이름순으로 정렬)
    students = Student_Master.objects.filter(data_status='Active').order_by('student_name')
    
    # 4. '조회된' 데이터를 'HTML'로 전달하기 위해 '사전(context)'에 담습니다.

    context = {
        'students': students,
    }

    return render(request, 'students/student_list.html', context)

# -----------------------------------------------------------------
# 2. [추가] '학생 상세 뷰' (화면 2)
# -----------------------------------------------------------------
def student_detail_view(request, student_id): # 'URL'로부터 'student_id'를 받음

    # 3. [핵심] 'student_id'를 '기본 키(pk)'로 사용하여 '학생 1명'의 정보를 '조회'합니다.
    #    (만약 'ID'가 '없으면' '자동'으로 '404 오류'를 띄웁니다.)
    student = get_object_or_404(Student_Master, pk=student_id)

    # 4. '조회된' 학생 1명의 정보를 'HTML'로 '전달'
    context = {
        'student': student,
    }

    # 5. 'HTML 파일'을 '렌더링'합니다. (HTML 파일은 '3단계'에서 생성)
    return render(request, 'students/student_detail.html', context)