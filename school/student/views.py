from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, CreateView, ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView, FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from core.models import Class
from .models import Enrollment
# from fees.models import FeesCollection
from core.models import AcademicYear
# from fees.forms import FeesCollectionForm
from .forms import EnrollmentForm, StudentFormStep1, StudentFormStep2, StudentUpdateForm, FeesCollectionForm
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from datetime import date
from django.utils import timezone
from django.shortcuts import get_object_or_404
from core.forms import current_academic_year
from school_fees.models import FeesCollection, TransportFees, FeesStructure

######## Enrollments Views
# Create a new Enrollment (Create)
# views.py

from django.http import JsonResponse
from .models import Student
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError


class EnrollmentDashboardView(ListView):
    model = Enrollment
    template_name = 'enrollment/enrollment_dashboard.html'
    context_object_name = 'enrollments'

# class StudentListView(ListView):
#     model = Student
#     template_name = 'enrollment/enrollment_student_list.html'
#     context_object_name = 'students'

#     def get_queryset(self):
#         queryset = Student.objects.all().filter(is_active=True).filter(enrollments__isnull=True).distinct()
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['standards'] = Standard.objects.all()
#         return context
    
   
# class EnrollmentFeesView(CreateView):
#     model = FeesCollection
#     template_name = 'enrollment/enrollment_fees.html'  # Template for creating a new student
#     form_class = FeesCollectionForm
#     success_url = reverse_lazy('enrollment-done')  # Redirect to the student list view on success
#     pk_url_kwarg = 'id'

#     def get(self, request, *args, **kwargs):
#         enrollment = Enrollment.objects.filter(id=self.kwargs['id'])
#         fees = FeesCollection.objects.filter(enrollment=enrollment.first())
#         if fees:
#             return HttpResponseRedirect(reverse('enrollment-detail', args=[enrollment.first().id]))             
#         else:
#             return super().get(request, *args, **kwargs)
        
#     def form_valid(self, form):
#         enrollment = Enrollment.objects.get(id=self.kwargs['id'])
#         fees = form.save(commit=False)
#         fees.enrollment = enrollment
#         fees.save()
#         return HttpResponseRedirect(reverse('enrollment-done', args=[enrollment.student.id]))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['student'] = Enrollment.objects.get(id=self.kwargs['id']).student
#         return context



############### Student Views

# # Create a new Enrollment (Create)
# class StudentCreateView(CreateView):
#     model = Student
#     template_name = 'student/student_form.html'  # Template for creating a new student
#     form_class = StudentForm    

#     def form_valid(self, form, *args, **kwargs):
#         # Save the form but don't commit it to the database yet
#         student = form.save(commit=False)
#         student.save()  # Now save it to the database
#         action = self.request.POST.get('action')
#         if action == 'save_and_enroll':
#             # Redirect to the 'enrollment-fees' page
#             return HttpResponseRedirect(reverse('enroll', kwargs={'id': student.id}))
#         return HttpResponseRedirect(reverse('student-list'))



class StudentFormStep1View(FormView):
    form_class = StudentFormStep1
    template_name = 'student/student_form_step1.html'

    def form_valid(self, form):
        # Save form data to the database
        student_data = form.cleaned_data
        
        # Convert date fields to strings (ISO format) for better serialization
        for field in ['date_of_birth', 'leaving_certificate_date']:
            if isinstance(student_data.get(field), date):
                student_data[field] = student_data[field].isoformat()  # Convert date to string

        # Create the student in the database
        student = Student.objects.create(**student_data)
        
        # Set the student ID for the next step
        self.success_url = reverse('enroll_step2', kwargs={'student_id': student.id})

        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url

class StudentFormStep2View(FormView):
    form_class = StudentFormStep2
    template_name = 'student/student_form_step2.html'


    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        if student.nationality:
            return redirect(reverse('enroll_step3', kwargs={'student_id': student.id}))
        else:
            return super().get(request, *args, **kwargs)
        

    def get_initial(self):
        # Retrieve the student object using the student_id from the URL
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        
            # return reverse('enroll_step3', kwargs={'id': student.id})

    def form_valid(self, form):
        # Retrieve the student object using the student_id from the URL
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)

        # Update student data with the new form values from Step 2
        student_data = form.cleaned_data
        for field, value in student_data.items():
            setattr(student, field, value)
        
        # Save the updated student instance
        student.save()

        # Redirect to the "enrollment done" URL with the student ID
        return redirect(reverse('enroll_step3', kwargs={'student_id': student.id}))

# class EnrollmentCreateView(CreateView):
#     model = Enrollment
#     template_name = 'student/enrollment_enroll.html'  # Template for creating a new student
#     form_class = EnrollmentForm
#     success_url = reverse_lazy('enrollment-done')  # Redirect to the student list view on success

#     def get(self, request, *args, **kwargs):        
#         student = Student.objects.get(id=self.kwargs.get('id'))
#         enrollment = Enrollment.objects.filter(student=student)        
#         if enrollment.exists():
#             return HttpResponseRedirect(reverse('enrollment-detail', args=[enrollment.first().id]))
#         else:
#             return super().get(request, *args, **kwargs)                
        
#     def form_valid(self, form):        
#         enrollment = form.save(commit=False)
#         enrollment.student = Student.objects.get(id=self.kwargs.get('id'))
#         enrollment.save()
#         return HttpResponseRedirect(reverse('enrollment-fees', args=[enrollment.id]))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['student'] = Student.objects.get(id=self.kwargs.get('id'))
#         return context


class EnrollmentCreateView(CreateView):
    model = Enrollment
    template_name = 'student/enrollment_enroll.html'  # Template for creating a new student
    form_class = EnrollmentForm

    def get(self, request, *args, **kwargs):        
        student = Student.objects.get(id=self.kwargs.get('student_id'))
        academic_year = current_academic_year()
        enrollment = Enrollment.objects.filter(student=student, academic_year=academic_year)
        # if enrollment.exists():
        #     return HttpResponseRedirect(reverse('enrollment-detail', args=[enrollment.first().id]))
        # else:
        return super().get(request, *args, **kwargs)                
        
    def form_valid(self, form):        
        enrollment = form.save(commit=False)
        enrollment.student = Student.objects.get(id=self.kwargs.get('student_id'))
        enrollment.academic_year = current_academic_year()
        enrollment.save()
        return HttpResponseRedirect(reverse('enroll_step4', kwargs={'enroll_id': enrollment.id}))
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = Student.objects.get(id=self.kwargs.get('student_id'))
        context['academic_year'] = current_academic_year()
        return context


class EnrollmentFeesView(CreateView):
    model = FeesCollection
    template_name = 'student/enrollment_fees_collection.html'  # Template for creating a new student
    form_class = FeesCollectionForm    

    # def get_success_url(self):
    #     # Access the 'enroll_id' from the URL kwargs
    #     enroll_id = self.kwargs.get(self.slug_url_kwarg)
    #     return reverse('enroll_step4', kwargs={'enroll_id': enroll_id})

    def form_valid(self, form):
        # Automatically set the enrollment based on the enroll_id from URL
        print("Fees Collection save commit False")
        fees_collection = form.save(commit=False)  
        fees_collection.enrollment = Enrollment.objects.get(id=self.kwargs.get('enroll_id'))
        fees_collection.fees_structure = FeesStructure.objects.get(class_name=fees_collection.enrollment.standard, academic_year=fees_collection.enrollment.academic_year)
        fees_collection.save()
        return HttpResponseRedirect(reverse('enrollment-done', kwargs={'enroll_id': fees_collection.enrollment.id}))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollment = Enrollment.objects.get(id=self.kwargs.get('enroll_id'))
        context['fees_structure'] = FeesStructure.objects.get(class_name=enrollment.standard, academic_year=enrollment.academic_year)        
        context['enrollment'] = enrollment
        return context
                
# class EnrollmentDoneView(View):
#     def get(self, request, **kwargs):
#         enrollment = Enrollment.objects.get(id=self.kwargs.get('enroll_id'))
#         first_name = enrollment.student.first_name.lower() if hasattr(enrollment.student, 'first_name') else ''
#         last_name = enrollment.student.last_name.lower() if hasattr(enrollment.student, 'last_name') else ''
#         aadhar_number = enrollment.student.adhar_number if hasattr(enrollment.student, 'adhar_number') else ''
        
#         # Generate username
#         username_prefix = (first_name[:4] if len(first_name) >= 4 else first_name + last_name[:4 - len(first_name)])
#         username_suffix = aadhar_number[-4:] if len(aadhar_number) >= 4 else ''
#         username = f"{username_prefix}{username_suffix}"
        
#         # Generate password
#         date_of_birth = enrollment.student.date_of_birth.strftime('%d%m%y') if hasattr(enrollment.student, 'date_of_birth') and enrollment.student.date_of_birth else '000000'
#         password = f"{username_prefix.capitalize()}@{date_of_birth}"
       
#         context= {
#             'student': enrollment.student,
#             'username': username,
#             'password': password
#             }    
#         return render(request, 'student/enrollment_done.html', context)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["name"] = 'akash'
#         return context
        
class EnrollmentDoneView(DetailView):
    model = Enrollment
    template_name = 'student/enrollment_done.html'
    context_object_name = 'enrollment'
    pk_url_kwarg = 'enroll_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollment = self.get_object()
        first_name = enrollment.student.first_name.lower() if hasattr(enrollment.student, 'first_name') else ''
        last_name = enrollment.student.last_name.lower() if hasattr(enrollment.student, 'last_name') else ''
        aadhar_number = enrollment.student.adhar_number if hasattr(enrollment.student, 'adhar_number') else ''
        
        # Generate username
        username_prefix = (first_name[:4] if len(first_name) >= 4 else first_name + last_name[:4 - len(first_name)])
        username_suffix = aadhar_number[-4:] if len(aadhar_number) >= 4 else ''
        username = f"{username_prefix}{username_suffix}"
        
        # Generate password
        date_of_birth = enrollment.student.date_of_birth.strftime('%d%m%y') if hasattr(enrollment.student, 'date_of_birth') and enrollment.student.date_of_birth else '000000'
        password = f"{username_prefix.capitalize()}@{date_of_birth}"
       
        context['username'] = username
        context['password'] = password
        return context


class EnrollmentlistView(ListView):
    model = Enrollment
    template_name = 'student/enrollment_list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        current_academic_year = AcademicYear.objects.get(start_date__lte=date.today(), end_date__gte=date.today())

        # enrollment = Enrollment.objects.all().filter(
        #     enrollment_date__gte=current_academic_year.start_date,
        #     enrollment_date__lte=current_academic_year.end_date
        # ) 

        enrollment = Enrollment.objects.filter(academic_year=current_academic_year)

        if self.request.GET:
            select_option = self.request.GET.get('search')
            select_ay = self.request.GET.get('ay')

            if select_ay:
                ay = AcademicYear.objects.get(name=select_ay)
                enrollment = Enrollment.objects.filter(academic_year=ay)

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
        context['academic_years'] = AcademicYear.objects.all()
        context['active_academic_year'] = AcademicYear.objects.get(start_date__lte=date.today(), end_date__gte=date.today())
        # context['standards'] = Class.objects.all()
        return context



class StudentPromoteListView(ListView):
    models = Student
    template_name = 'student/student_promote.html'
    context_object_name = 'promots'

    def get_queryset(self):
        students = Student.objects.all().filter(enrollments__isnull=False)
        return students.order_by('id')




class EnrollmentDetailView(DetailView):
    model = Enrollment
    template_name = 'student/enrollment_detail.html'
    context_object_name = 'enrollment'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['standards'] = Class.objects.all()
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
    


def test(request):
    return render(request, 'student/enrollment_admisison_recipt.html')


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
        context['standards'] = Class.objects.all()
        return context






# List all students (Read - List)
class StudentListView(ListView):
    model = Student
    # template_name = 'student_list.html'  # Template to render the list of students
    context_object_name = 'students'
    
    def get_queryset(self):
        students = Student.objects.all()
        if  self.request.GET:
            select_option = self.request.GET.get('search')
            if select_option:
                if select_option.lower() == 'enrolled':
                    students = students.filter(enrollments__isnull=False).distinct()
                elif select_option.lower() == 'not-enrolled':
                    students = students.filter(enrollments__isnull=True).distinct()          
        return students.order_by('id')
    
    def post(self, request, *args, **kwargs):
        student_id = request.POST.get('student_id')
        student = Student.objects.get(id=student_id)
        
        if student.enrollments.exists():
            # Prevent deactivation of active students and show a message
            messages.warning(request, 'You cannot deactivate an Enrolled student.')
            return HttpResponseRedirect(reverse('student-list'))   # Redirect to the student list view
        # Deactivate the student
        student.save()
        messages.success(request, f'Student {student} has been successfully deactivated.')
        return HttpResponseRedirect(reverse('student-list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['ac_year'] = AcademicYear.objects.get(is_active=True)
        return context



class StudentDetailView(DetailView):
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'enrollment'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    permission_required = 'core.view_student'


# Update an existing student (Update)
class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'student/student_update.html'  # Reusing the form template for editing
    form_class = StudentUpdateForm
    success_url = reverse_lazy('student-list')  # Redirect to the student list view on success
    permission_required = 'core.change_student'

# class StudentDeleteView(DeleteView):
#     model = Student
#     template_name = 'student/student_delete_confirm.html'  # The confirmation page template
#     context_object_name = 'student'  # The context variable name for the student
#     # Redirect to the student list after successful deletion
#     success_url = reverse_lazy('student-archive-list')


# Archive Student
class StudentArchiveListView(ListView):
    model = Student
    template_name = 'student/student_archive_list.html'  # Template to render the list of students
    context_object_name = 'students'
    permission_required = 'core.view_student'
    
    def get_queryset(self):
        students = Student.objects.all().filter(is_active=False)
        if  self.request.GET:
            select_class = self.request.GET.get('class')
            if select_class and select_class != 'no-class':
                students = students.filter(standard__id__icontains=select_class)
        return students.order_by('id')
    
    def post(self, request, *args, **kwargs):
        student_id = request.POST.get('student_id')
        student = Student.objects.get(id=student_id)
        # Activate the student
        student.is_active = True
        student.save()
        messages.success(request, f'Student {student} has been successfully Activated.')
        return HttpResponseRedirect(reverse('student-archive-list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.all().filter(is_active=False).count()
        context['standards'] = Class.objects.all()
        return context
