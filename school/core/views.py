from django.shortcuts import render
from .models import Student, Teacher, Standard, Subject
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import StudentForm, TeacherForm, StandardForm
from django.http import JsonResponse
from django.template.loader import render_to_string


def dashboard(request):
    return render(request, 'core/dashboard.html')

def login(request):
    return render(request, 'core/login.html')

def reset_password(request):
    return render(request, 'core/reset_password.html')


def logout(request):
    return render(request, 'core/logout.html')

def profile(request):
    return render(request, 'core/profile.html')



############### Student Views
# List all students (Read - List)
class StudentListView(ListView):
    model = Student
    template_name = 'core/student_list.html'  # Template to render the list of students
    context_object_name = 'students'
    paginate_by = 10



    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            class_id = request.POST.get('class_id')
            gender = request.POST.get('gender')

            students = Student.objects.all()
            if class_id:
                students = students.filter(standard_id=class_id)
            if gender:
                students = students.filter(gender=gender)
            print(class_id)
            print(students)
            # Render the filtered list into HTML
            html = render_to_string('core/partials/student_list.html', {'students': students})
            return JsonResponse({'html': html})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.all().count()
        context['standards'] = Standard.objects.all()
        return context


class StudentDetailView(DetailView):
    model = Student
    template_name = 'core/student_detail.html'
    context_object_name = 'student'
    slug_field = 'id'
    slug_url_kwarg = 'id'

# Create a new student (Create)
class StudentCreateView(CreateView):
    model = Student
    template_name = 'core/student_form.html'  # Template for creating a new student
    form_class = StudentForm
    success_url = reverse_lazy('student-list')  # Redirect to the student list view on success

# Update an existing student (Update)
class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'core/student_form.html'  # Reusing the form template for editing
    form_class = StudentForm
    success_url = reverse_lazy('student-list')  # Redirect to the student list view on success

# Delete a student (Delete)
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_confirm_delete.html'  # Template to confirm deletion
    success_url = reverse_lazy('student-list')  # Redirect to the student list view on success



############### Teacher Views
# List all Teacher (Read - List)
class TeacherListView(ListView):
    model = Teacher
    template_name = 'core/teacher_list.html'  # Template to render the list of students
    context_object_name = 'teachers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_teacher'] = Teacher.objects.all().count()
        return context


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'core/teacher_detail.html'
    context_object_name = 'teacher'
    # slug_url_kwarg = 'student_id'


# Create a new Teacher (Create)
class TeacherCreateView(CreateView):
    model = Teacher
    template_name = 'core/teacher_form.html'  # Template for creating a new Teaher
    form_class = TeacherForm
    success_url = reverse_lazy('teacher-list')  # Redirect to the Teaher list view on success

# Update an existing Teacher (Update)
class TeacherUpdateView(UpdateView):
    model = Teacher
    template_name = 'core/teacher_form.html'  # Reusing the form template for editing
    form_class = TeacherForm
    success_url = reverse_lazy('teacher-list')  # Redirect to the Teaher list view on success

# Delete a Teacher (Delete)
class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'teacher_confirm_delete.html'  # Template to confirm deletion
    success_url = reverse_lazy('teacher-list')  # Redirect to the Teaher list view on success




############### Standard Views
class StandardListView(ListView):
    model = Standard
    template_name = 'core/standard_list.html'  # Template to render the list of students
    context_object_name = 'standards'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_standard'] = Standard.objects.all().count()
        return context


class StandardDetailView(DetailView):
    model = Standard
    template_name = 'core/standard_detail.html'
    context_object_name = 'standard'
    # slug_url_kwarg = 'student_id'


# Create a new Standard (Create)
class StandardCreateView(CreateView):
    model = Standard
    template_name = 'core/standard_form.html'  # Template for creating a new Standard
    form_class = StandardForm
    success_url = reverse_lazy('standard-list')  # Redirect to the Teaher list view on success

# Update an existing Standard (Update)
class StandardUpdateView(UpdateView):
    model = Standard
    template_name = 'core/standard_form.html'  # Reusing the form template for editing
    form_class = StandardForm
    success_url = reverse_lazy('standard-list')  # Redirect to the Standard list view on success

# Delete a Teacher (Delete)
class StandardDeleteView(DeleteView):
    model = Standard
    template_name = 'standard_confirm_delete.html'  # Template to confirm deletion
    success_url = reverse_lazy('standard-list')  # Redirect to the Standard list view on success
