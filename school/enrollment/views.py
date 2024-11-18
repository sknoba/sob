from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, CreateView, ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from core.models import Student, Standard
from .models import Enrollment
from fees.models import FeesCollection
from fees.forms import FeesCollectionForm
from .forms import EnrollmentForm   
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q


######## Enrollments Views
# Create a new Enrollment (Create)
# views.py

from django.http import JsonResponse
from .models import Student
from django.template.loader import render_to_string



class EnrollmentDashboardView(ListView):
    model = Enrollment
    template_name = 'enrollment/enrollment_dashboard.html'
    context_object_name = 'enrollments'

class StudentListView(ListView):
    model = Student
    template_name = 'enrollment/enrollment_student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        queryset = Student.objects.all().filter(is_active=True).filter(enrollments__isnull=True).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['standards'] = Standard.objects.all()
        return context
    
class EnrollmentlistView(ListView):
    model = Enrollment
    template_name = 'enrollment/enrollment_list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        enrollment = Enrollment.objects.all()
        if self.request.GET:
            select_option = self.request.GET.get('search')

            if select_option:
                select_option = select_option.lower()

                if select_option == 'cancelled':
                    # Filter for cancelled enrollments (where cancel_enroll is True)
                    enrollment = enrollment.filter(cancel_enroll=True)

                elif select_option == 'incompleted':
                    # Filter for enrollments without a corresponding FeesCollection
                    enrollment = enrollment.filter(fees_collections__isnull=True)

                elif select_option == 'done':
                    # Filter for enrollments that are neither cancelled nor incomplete
                    enrollment = enrollment.filter(
                        Q(cancel_enroll=False) & Q(fees_collections__isnull=False)
                    ).distinct()

        return enrollment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['standards'] = Standard.objects.all()
        return context
    

# Archive Student
class EnrollmentCancelListView(ListView):
    model = Enrollment
    template_name = 'enrollment/enrollment_cancel_list.html'  # Template to render the list of students
    context_object_name = 'enrollments'
    
    def get_queryset(self):
        enrollment = Enrollment.objects.all().filter(cancel_enroll=True)
        # if  self.request.GET:
        #     select_class = self.request.GET.get('class')
        #     if select_class and select_class != 'no-class':
        #         students = students.filter(standard__id__icontains=select_class)
        return enrollment.order_by('id')
    
    # def post(self, request, *args, **kwargs):
    #     student_id = request.POST.get('student_id')
    #     student = Student.objects.get(id=student_id)
    #     # Activate the student
    #     student.is_active = True
    #     student.save()
    #     messages.success(request, f'Student {student} has been successfully Activated.')
    #     return HttpResponseRedirect(reverse('student-archive-list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.all().filter(is_active=False).count()
        context['standards'] = Standard.objects.all()
        return context






class EnrollmentDetailView(DetailView):
    model = Enrollment
    template_name = 'enrollment/enrollment_detail.html'
    context_object_name = 'enrollment'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['standards'] = Standard.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        # Get the specific Enrollment object
        enrollment = self.get_object()
        
        if not enrollment.cancel_enroll:
            enrollment.cancel_enroll = True
            enrollment.save()
            messages.success(request, 'Enrollment has been successfully canceled.')
        else:
            # If the enrollment was already canceled, show a different message
            messages.warning(request, 'This enrollment is already canceled.')

        return redirect('enrollment_detail', enrollment.id)
    
class EnrollmentCreateView(CreateView):
    model = Enrollment
    template_name = 'enrollment/enrollment_enroll.html'  # Template for creating a new student
    form_class = EnrollmentForm
    success_url = reverse_lazy('enrollment-done')  # Redirect to the student list view on success

    def get(self, request, *args, **kwargs):        
        student = Student.objects.get(id=self.kwargs.get('id'))
        enrollment = Enrollment.objects.filter(student=student)        
        if enrollment.exists():
            return HttpResponseRedirect(reverse('enrollment-detail', args=[enrollment.first().id]))
        else:
            return super().get(request, *args, **kwargs)                
        
    def form_valid(self, form):        
        enrollment = form.save(commit=False)
        enrollment.student = Student.objects.get(id=self.kwargs.get('id'))
        enrollment.save()
        return HttpResponseRedirect(reverse('enrollment-fees', args=[enrollment.id]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = Student.objects.get(id=self.kwargs.get('id'))
        return context

class EnrollmentFeesView(CreateView):
    model = FeesCollection
    template_name = 'enrollment/enrollment_fees.html'  # Template for creating a new student
    form_class = FeesCollectionForm
    success_url = reverse_lazy('enrollment-done')  # Redirect to the student list view on success
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        enrollment = Enrollment.objects.filter(id=self.kwargs['id'])
        fees = FeesCollection.objects.filter(enrollment=enrollment.first())
        if fees:
            return HttpResponseRedirect(reverse('enrollment-detail', args=[enrollment.first().id]))             
        else:
            return super().get(request, *args, **kwargs)
        
    def form_valid(self, form):
        enrollment = Enrollment.objects.get(id=self.kwargs['id'])
        fees = form.save(commit=False)
        fees.enrollment = enrollment
        fees.save()
        return HttpResponseRedirect(reverse('enrollment-done', args=[enrollment.student.id]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = Enrollment.objects.get(id=self.kwargs['id']).student
        return context



class EnrollmentDoneView(View):
    def get(self, request, **kwargs):
        student = Student.objects.get(id=self.kwargs.get('id'))
        context= {
            'student': student
            }
        return render(request, 'enrollment/enrollment_done.html', context)
