from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .models import Student, UserProfile, Standard, Subject, AcademicYear
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from .forms import StudentForm, StandardForm, UserProfileForm, AcademicYearForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from fees.models import FeesCollection
from fees.forms import FeesCollectionForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q




from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
    
@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def profile(request):
    return render(request, 'core/profile.html')


############### Student Views

# Create a new Enrollment (Create)
class StudentCreateView(CreateView):
    model = Student
    template_name = 'core/student_form.html'  # Template for creating a new student
    form_class = StudentForm    

    def form_valid(self, form, *args, **kwargs):
        # Save the form but don't commit it to the database yet
        student = form.save(commit=False)
        student.save()  # Now save it to the database
        action = self.request.POST.get('action')
        if action == 'save_and_enroll':
            # Redirect to the 'enrollment-fees' page
            return HttpResponseRedirect(reverse('enroll', kwargs={'id': student.id}))
        return HttpResponseRedirect(reverse('student-list'))



# List all students (Read - List)
class StudentListView(PermissionRequiredMixin, ListView):
    model = Student
    template_name = 'core/student_list.html'  # Template to render the list of students
    context_object_name = 'students'
    permission_required = 'core.view_student'
    
    def get_queryset(self):
        students = Student.objects.all()
        if  self.request.GET:
            select_option = self.request.GET.get('search')
            if select_option:
                if select_option.lower() == 'enrolled':
                    students = students.filter(enrollments__isnull=False).distinct()
                elif select_option.lower() == 'not-enrolled':
                    students = students.filter(enrollments__isnull=True).distinct()          
        return students.order_by('id').filter(is_active=True)
    
    def post(self, request, *args, **kwargs):
        student_id = request.POST.get('student_id')
        student = Student.objects.get(id=student_id)
        
        if student.enrollments.exists():
            # Prevent deactivation of active students and show a message
            messages.warning(request, 'You cannot deactivate an Enrolled student.')
            return HttpResponseRedirect(reverse('student-list'))   # Redirect to the student list view

        # Deactivate the student
        student.is_active = False
        student.save()
        messages.success(request, f'Student {student} has been successfully deactivated.')
        return HttpResponseRedirect(reverse('student-list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ac_year'] = AcademicYear.objects.get(is_active=True)
        return context



class StudentDetailView(PermissionRequiredMixin, DetailView):
    model = Student
    template_name = 'core/student_detail.html'
    context_object_name = 'enrollment'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    permission_required = 'core.view_student'


# Update an existing student (Update)
class StudentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Student
    template_name = 'core/student_form.html'  # Reusing the form template for editing
    form_class = StudentForm
    success_url = reverse_lazy('student-list')  # Redirect to the student list view on success
    permission_required = 'core.change_student'

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'core/student_delete_confirm.html'  # The confirmation page template
    context_object_name = 'student'  # The context variable name for the student
    # Redirect to the student list after successful deletion
    success_url = reverse_lazy('student-archive-list')


# Archive Student
class StudentArchiveListView(PermissionRequiredMixin, ListView):
    model = Student
    template_name = 'core/student_archive_list.html'  # Template to render the list of students
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
        context['standards'] = Standard.objects.all()
        return context



########## Teacher Views
# List all Teacher (Read - List)
class TeacherListView(ListView):
    model = UserProfile
    template_name = 'core/teacher_list.html'  # Template to render the list of students
    context_object_name = 'teachers'
    paginate_by = 10

    def get_queryset(self):
        teacher = UserProfile.objects.filter(acc_type='TS')
        if  self.request.GET:
            teacher_query = self.request.GET.get('search')
            if teacher_query:
                teacher = teacher.filter(first_name__icontains=teacher_query) or teacher.filter(last_name__icontains=teacher_query)
        return teacher
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_teacher'] = UserProfile.objects.filter(acc_type='TS').count()
        return context


class TeacherDetailView(DetailView):
    model = UserProfile
    template_name = 'core/teacher_detail.html'
    context_object_name = 'teacher'
    slug_url_kwarg = 'acc_id'
    slug_field = 'acc_id'


# Update an existing Teacher (Update)
class TeacherUpdateView(UpdateView):
    model = UserProfile
    template_name = 'core/teacher_form.html'  # Reusing the form template for editing
    form_class = UserProfileForm
    slug_url_kwarg = 'acc_id'
    slug_field = 'acc_id'
    success_url = reverse_lazy('teacher-list')  # Redirect to the Teaher list view on success


########## Staff Views
# List all Teacher (Read - List)
class StaffListView(ListView):
    model = UserProfile
    template_name = 'core/staff_list.html'  # Template to render the list of students
    context_object_name = 'staffs'
    paginate_by = 10

    def get_queryset(self):
        teacher = UserProfile.objects.filter(acc_type='NT')
        if  self.request.GET:
            teacher_query = self.request.GET.get('search')
            if teacher_query:
                teacher = teacher.filter(first_name__icontains=teacher_query) or teacher.filter(last_name__icontains=teacher_query)
        return teacher
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_staff'] = UserProfile.objects.filter(acc_type='NT').count()
        return context
    
class StaffDetailView(DetailView):
    model = UserProfile
    template_name = 'core/staff_detail.html'
    context_object_name = 'staff'
    slug_url_kwarg = 'acc_id'

    def get_object(self):
        acc_id = self.kwargs.get('acc_id')
        return get_object_or_404(UserProfile, acc_id=acc_id)


# Update an existing Teacher (Update)
class StaffUpdateView(UpdateView):
    model = UserProfile
    template_name = 'core/staff_form.html'  # Reusing the form template for editing
    form_class = UserProfileForm
    slug_url_kwarg = 'acc_id'
    slug_field = 'acc_id'
    success_url = reverse_lazy('staff-list')  # Redirect to the Teaher list view on success





############### Standard Views
class StandardListView(PermissionRequiredMixin, ListView):
    model = Standard
    template_name = 'core/standard_list.html'  # Template to render the list of students
    context_object_name = 'standards'
    permission_required = 'core.view_standard'

    def test_func(self):
        return self.request.user.is_staff 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_standard'] = Standard.objects.all().count()
        return context


class StandardDetailView(PermissionRequiredMixin, DetailView):
    model = Standard
    template_name = 'core/standard_detail.html'
    context_object_name = 'standard'
    permission_required = 'core.view_standard'


# Create a new Standard (Create)
class StandardCreateView(PermissionRequiredMixin, CreateView):
    model = Standard
    template_name = 'core/standard_form.html'  # Template for creating a new Standard
    form_class = StandardForm
    success_url = reverse_lazy('standard-list')  # Redirect to the Teaher list view on success
    permission_required = 'core.add_standard'

# Update an existing Standard (Update)
class StandardUpdateView(PermissionRequiredMixin, UpdateView):
    model = Standard
    template_name = 'core/standard_form.html'  # Reusing the form template for editing
    form_class = StandardForm
    success_url = reverse_lazy('standard-list')  # Redirect to the Standard list view on success
    permission_required = 'core.change_standard'

# Delete a Teacher (Delete)
class StandardDeleteView(PermissionRequiredMixin, DeleteView):
    model = Standard
    template_name = 'standard_confirm_delete.html'  # Template to confirm deletion
    success_url = reverse_lazy('standard-list')  # Redirect to the Standard list view on success
    permission_required = 'core.delete_standard'






###############Access Management
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserProfileForm, UserAccessUpdateForm, UserCreateAccessForm
from django.http import Http404
from django.core.exceptions import PermissionDenied

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)

def accessmanagement(request):
    return render(request, 'core/access_management.html')


class UserListView(ListView):
    model = UserProfile
    template_name = 'core/access_user_list.html'
    context_object_name = 'users'

class UserRegisterView(FormView):
    template_name = 'core/access_user_register.html'
    form_class = UserCreationForm
    
    def form_valid(self, form):
        user = form.save() 
        return HttpResponseRedirect(reverse('access-user-access', kwargs={'user_id': user.id}))

class UserCreateAccessView(UpdateView):
    model = User
    form_class = UserCreateAccessForm
    template_name = 'core/access_user_access.html'

    def get_object(self):
        user_id = self.kwargs['user_id']
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("User not found")

    def form_valid(self, form):        
        form.save()
        return self.render_to_response(self.get_context_data(success=True))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.get_object().username
        return context
    

class UserAccessUpdateView(UpdateView):
    model = User
    form_class = UserAccessUpdateForm
    template_name = 'core/access_user_access_update.html'

    def get_object(self):
        user_id = self.kwargs['user_id']
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("User not found")

    def form_valid(self, form):        
        form.save()
        return self.render_to_response(self.get_context_data(success=True))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.get_object().username
        return context
    
        
class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'core/access_user_profile_update.html'
    success_url = reverse_lazy('access-user-list')  # Redirect after a successful update

    def get_object(self):
        user_id = self.kwargs['user_id']
        try:
            return UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            raise Http404("User not found")
        

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'core/access_user_confirm_delete.html'
    success_url = reverse_lazy('access-user-list')  # Redirect after successful deletion

    def get_object(self):
        user_id = self.kwargs.get("user_id")  # Retrieve 'user_id' from URL
        return User.objects.get(id=user_id)

    def test_func(self):
        return self.request.user.is_superuser  # Only SuperAdmin can delete users
    

### Group Views
class GroupListView(ListView):
    model = Group
    template_name = 'core/access_group_list.html'
    context_object_name = 'groups'
    paginate_by = 10

    def get_queryset(self):
        group = Group.objects.all()
        if  self.request.GET:
            group_query = self.request.GET.get('search')
            if group_query:
                group = group.filter(name__icontains=group_query)
        return group
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_group'] = Group.objects.all().count()
        return context

class GroupCreateView(CreateView):
    model = Group
    template_name = 'core/access_group_form.html'
    fields = ['name', 'permissions']
    success_url = reverse_lazy('access-group-list')

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'core/access_group_form.html'
    fields = ['name', 'permissions']
    success_url = reverse_lazy('access-group-list')

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'core/access_group_confirm_delete.html'
    success_url = reverse_lazy('access-group-list')  # Redirect after successful deletion

    def get_object(self):
        group_id = self.kwargs.get("pk")  # Retrieve 'user_id' from URL
        return Group.objects.get(id=group_id)

    def test_func(self):
        return self.request.user.is_superuser  # Only SuperAdmin can delete users
    

##### Academic Year Views

class AcademicYearListView(ListView):
    model = AcademicYear
    template_name = 'core/academic_year_list.html'
    context_object_name = 'academic_years'

class AcademicYearDetailView(DetailView):
    model = AcademicYear
    template_name = 'core/academic_year_detail.html'
    context_object_name = 'academic_year'

class AcademicYearCreateView(CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'core/academic_year_form.html'
    success_url = reverse_lazy('academic-year-list')

    def form_valid(self, form):
        messages.success(self.request, "Academic year created successfully!")
        return super().form_valid(form)

class AcademicYearUpdateView(UpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'core/academic_year_form.html'
    success_url = reverse_lazy('academic-year-list')

    def form_valid(self, form):
        messages.success(self.request, "Academic year updated successfully!")
        return super().form_valid(form)

class AcademicYearDeleteView(DeleteView):
    model = AcademicYear
    template_name = 'core/academic_year_confirm_delete.html'
    success_url = reverse_lazy('academic-year-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Academic year and its related records deleted successfully!")
        return super().delete(request, *args, **kwargs)
