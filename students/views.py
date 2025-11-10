from django.shortcuts import render
from .models import Student_Master  # '학생 모델' import

# '학생 목록' 기능
def student_list_view(request):
    
    # '활성(Active)' 학생만 '이름순'으로 '조회'
    students = Student_Master.objects.filter(data_status='Active').order_by('student_name')
    
    # '조회된' 데이터를 'HTML'로 '전달'
    context = {
        'students': students,
    }
    
    # 'HTML 파일'을 '렌더링'
    return render(request, 'students/student_list.html', context)