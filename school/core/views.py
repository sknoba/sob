from django.shortcuts import render
from .models import Student
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import StudentForm


# List all students (Read - List)
class StudentListView(ListView):
    model = Student
    template_name = 'core/student_list.html'  # Template to render the list of students
    context_object_name = 'students'


class StudentDetailView(DetailView):
    model = Student
    template_name = 'core/student.html'
    context_object_name = 'student'
    # slug_url_kwarg = 'student_id'


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
