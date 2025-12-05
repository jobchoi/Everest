from collections import Counter
from django.shortcuts import render, get_object_or_404, redirect
# [수정] 'AI'가 '분석'할 '모든' 모델을 'import'
from .models import (
    Student_Master, Activity_Log, 
    Goal_History, Teacher_Master, Category_Master, Department_Master
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


    # 4. [수정] 'POST' (저장) 로직 (H-191)
    if request.method == 'POST':
        data = json.loads(request.body)
        
        content = data.get('content_text', '')
        tags = data.get('tags', []) 
        teacher_id = data.get('teacher_id')
        category_id = data.get('category_id')
        activity_date = data.get('activity_date') 

        teacher = get_object_or_404(Teacher_Master, pk=teacher_id)
        category = get_object_or_404(Category_Master, pk=category_id)

        # 8. [H-207 수정] '새' 로그를 '변수'에 '저장'합니다.
        new_activity = Activity_Log.objects.create(
            student_uuid=student,
            teacher_id=teacher,
            category_id=category,
            activity_date=activity_date,
            content_text=content,
            activity_tags=tags
        )
        
        # 9. [H-207 수정] '단순 성공' '대신', '방금' '생성'한 '객체'의 '정보'를 'JSON'으로 '반환'합니다.
        #    (JS가 'AJAX 확인'에 '사용'할 '재료')
        return JsonResponse({
            'status': 'success', 
            'message': '활동 로그가 성공적으로 저장되었습니다.',
            'new_activity': {
                'category_name': new_activity.category_id.category_name,
                'activity_date': new_activity.activity_date,
                'content_text': new_activity.content_text,
                'teacher_name': new_activity.teacher_id.teacher_name,
                'activity_tags': new_activity.activity_tags
            }
        })

    # 3. [추가] '학생'과 '연관된' '활동 로그'를 '모두' 조회.
    #    (최신순으로 정렬)
    activities = Activity_Log.objects.filter(student_uuid=student).order_by('-activity_date')
    goals = Goal_History.objects.filter(student_uuid=student).order_by('-record_date')

    # 4. [추가] '하드코딩'을 '해결'하기 위해, '모든' 교사와 '모든' 카테고리를 'DB'에서 '조회'
    all_teachers = Teacher_Master.objects.all()
    all_categories = Category_Master.objects.all()


    all_tags = []
    for activity in activities:
        tags = activity.activity_tags
        
        # [핵심] tags가 만약 문자열로 들어왔다면 리스트로 변환 시도 (방어 코딩)
        if isinstance(tags, str):
            try:
                tags = json.loads(tags.replace("'", '"')) # 혹시 모를 작은따옴표 처리
            except:
                tags = [] # 변환 실패 시 빈 리스트

        # 리스트인 경우에만 합치기
        if tags and isinstance(tags, list):
            all_tags.extend(tags)
            
    # 3. 빈도수 계산
    tag_counts = Counter(all_tags).most_common(5)
    
    # 4. 차트 데이터 생성
    # (데이터가 없으면 빈 리스트가 들어가서 차트가 숨겨짐 -> JS 로직)
    chart_labels = [item[0] for item in tag_counts]
    chart_data = [item[1] for item in tag_counts]

    # 5. [수정] '조회된' '모든' 정보를 'HTML'로 '전달'
    context = {
        'student': student,
        'activities': activities,   
        'goals': goals,             
        'all_teachers': all_teachers,       # (추가)
        'all_categories': all_categories,   # (추가)
        'chart_labels': json.dumps(chart_labels, ensure_ascii=False),
        'chart_data': json.dumps(chart_data)
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

