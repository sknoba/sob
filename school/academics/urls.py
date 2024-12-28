from django.urls import path, include
from .views import *


urlpatterns = [
        path('dashboard', DashboardView.as_view(), name='academic-dashboard'),
        path('exams', ExamCreateView.as_view(), name='academic-exams'),
        path('<int:exam_id>/exam-detail', ExamDetailView.as_view(), name='academic-exam-detail'),
        path('score', ExamScoreClassListView.as_view(), name='academic-score'),
        path('<int:exam_id>/score-student-list', StudentListView.as_view(), name='academic-score-student-list'),        
        path('subject-score-add', StudentListView.as_view(), name='academic-subject-score-add'),
        path('scorecard-student-list', ScoreCardStudentListView.as_view(), name='academic-scorecard-students-list'),
        path('<int:student_id>/academic-score-card', ScoreCardDetailView.as_view(), name='academic-score-card'),
]