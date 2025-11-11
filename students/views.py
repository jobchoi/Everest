from django.shortcuts import render, get_object_or_404
# 1. [수정] 'AI'가 '분석'할 '모든' 모델을 'import'
from .models import Student_Master, Activity_Log, Goal_History


# Create your views here.
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

    # 2. 'student_id'를 '기본 키(pk)'로 사용하여 '학생 1명'의 정보를 '조회'.
    #    (만약 'ID'가 '없으면' '자동'으로 '404 오류'를 띄웁니다.)
    student = get_object_or_404(Student_Master, pk=student_id)

    # 3. [추가] '학생'과 '연관된' '활동 로그'를 '모두' 조회.
    #    (최신순으로 정렬)
    activities = Activity_Log.objects.filter(student_uuid=student).order_by('-activity_date')

    # 4. [추가] '학생'과 '연관된' '목표 이력'을 '모두' 조회.
    #    (최신순으로 정렬)
    goals = Goal_History.objects.filter(student_uuid=student).order_by('-record_date')

    # 5. [수정] '조회된' '모든' 정보를 'HTML'로 '전달'
    context = {
        'student': student,
        'activities': activities, # (추가)
        'goals': goals            # (추가)
    }

    # 6. 'HTML 파일'을 '렌더링'
    return render(request, 'students/student_detail.html', context)