from django.shortcuts import render, get_object_or_404
# [수정] 'AI'가 '분석'할 '모든' 모델을 'import'
from .models import (
    Student_Master, Activity_Log, 
    Goal_History, Teacher_Master, Category_Master
)


# 'JSON' 응답(JsonResponse)과 'JSON' 파싱(json)을 'import' 합니다.
from django.http import JsonResponse
import json

# 2. [수정] 'B-an(AI)' 엔진(KoNLPy)을 'import' 합니다.
from konlpy.tag import Okt

# Create your views here.
# -----------------------------------------------------------------
# 1. (추가)] '항해일지 134번' (화면 1: 학생 목록 뷰)
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
    goals = Goal_History.objects.filter(student_uuid=student).order_by('-record_date')

    # 4. [추가] '하드코딩'을 '해결'하기 위해, '모든' 교사와 '모든' 카테고리를 'DB'에서 '조회'
    all_teachers = Teacher_Master.objects.all()
    all_categories = Category_Master.objects.all()

    # 5. [수정] '조회된' '모든' 정보를 'HTML'로 '전달'
    context = {
        'student': student,
        'activities': activities,   
        'goals': goals,             
        'all_teachers': all_teachers,       # (추가)
        'all_categories': all_categories,   # (추가)
    }

    # 6. 'HTML 파일'을 '렌더링'
    return render(request, 'students/student_detail.html', context)


# -----------------------------------------------------------------
# 3. [추가] 'Sprint 1 - 5.4단계' (AI(B-an) API 뷰)
# -----------------------------------------------------------------
def api_extract_tags_view(request):
    
    # 4. [보안] 'POST' 요청(JavaScript Fetch)이 '아니면' '거부'합니다.
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST 요청만 허용됩니다.'}, status=405)

    try:
        # 5. 'JavaScript'가 'POST'로 보낸 'JSON' 데이터를 '읽습니다'.
        data = json.loads(request.body)
        raw_text = data.get('text', '') # 'text' 키가 없으면 '빈 값'

        if not raw_text:
            return JsonResponse({'status': 'error', 'message': '분석할 텍스트가 없습니다.'}, status=400)

        # 6. [B-an 실행] '항해일지 89번'에서 '설치'한 'KoNLPy(Okt)'를 '실행'합니다.
        okt = Okt()
        # '명사(Nouns)'만 '추출'하여 '태그'로 사용합니다. (B-an의 '한계', H-22)
        tags = okt.nouns(raw_text)

        # 7. [GIGO 방지] '중복' 태그를 '제거'하고 2글자 '이상'만 '필터링'합니다.
        #    (예: '학생', '것', '수' 등 1글자 단어 '제거')
        processed_tags = sorted(list(set([tag for tag in tags if len(tag) > 1])))

        # 8. [성공] '프론트엔드(JS)'로 'JSON' 데이터(태그 목록)를 '반환'합니다.
        return JsonResponse({'status': 'success', 'tags': processed_tags})

    except Exception as e:
        # 9. [오류] 'B-an' 엔진이 '죽거나' '오류'가 나면, '서버 오류'를 '반환'합니다.
        return JsonResponse({'status': 'error', 'message': f'AI 분석 중 오류 발생: {e}'}, status=500)

