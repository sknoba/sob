from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from .models import Exams, ExamScore
from core.models import Class
from .forms import ExamsForm
from student.models import Enrollment
from core.forms import current_academic_year
from django.urls import reverse_lazy



def exams(request):
    return render(request, 'academics/academics_exams.html')

def score(request):
    return render(request, 'academics/academics_score.html')

def score_card(request):
    return render(request, 'academics/academic_score_card.html')

class DashboardView(TemplateView):
    template_name = 'academics/academic_dashboard.html'  # Template to render the list of students


class ExamCreateView(CreateView):
    model = Exams
    template_name = 'academics/academics_exams.html'  # Template to render the list of students
    form_class = ExamsForm    
    success_url = reverse_lazy('academic-exams')

    def form_valid(self, form):
        form.instance.academic_year = current_academic_year()
        return super().form_valid(form)
    
    def form_invalid(self, form):        
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exams'] = Exams.objects.all().order_by('id').order_by('class_name')
        context['classes'] = Class.objects.all()
        return context

class ExamDetailView(DetailView):
    model = Exams
    template_name = 'academics/academic_exam_detail.html'  # Template to render the list of students
    context_object_name = 'exam'  # Name of the list as a template variable
    pk_url_kwarg = 'exam_id' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context
    

class ExamScoreClassListView(ListView):
    model = Exams
    template_name = 'academics/academics_score.html'  # Template to render the list of students
    context_object_name = 'exams'  # Name of the list as a template variable        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['classes'] = Class.objects.all()       
        return context


class StudentListView(ListView):
    model = Enrollment
    template_name = 'academics/academic_student_list.html'  # Template to render the list of students
    context_object_name = 'students'  # Name of the list as a template variable    
    url_kwarg = 'exam_id'

    def get_queryset(self):
        exam = Exams.objects.get(id=self.kwargs.get('exam_id'))
        students = Enrollment.objects.filter(standard=exam.class_name)
        return students
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['classes'] = Class.objects.all() 
        context['exam'] = Exams.objects.get(id=self.kwargs.get('exam_id'))      
        return context
    

class ScoreCardStudentListView(ListView):
    model = Enrollment
    template_name = 'academics/academic_score_card_students.html'  # Template to render the list of students
    context_object_name = 'students'  # Name of the list as a template variable    

    # def get_queryset(self):
    #     students = Enrollment.objects.filter(standard=self.kwargs.get('standard'))
    #     return students
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        # context['classes'] = Class.objects.all() 
        # context['standard'] = self.kwargs.get('standard')      
        return context
    
class ScoreCardDetailView(View):
    template_name = 'academics/academic_score_card.html'  # Template to render the list of students
    pk_url_kwarg = 'student_id' 

    def get_student(self):
        student = Enrollment.objects.get(id=self.kwargs.get('student_id'))
        # exam_score = Exams.objects.filter(exam_score.student=student)
        # print(exam_score)
        # exam_score = Exams.objects.filter(exam_score.student=student)
        # return {'student': student, 'exam_score': exam_score}
        return {'student': student}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_student())
