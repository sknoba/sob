from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.models import Group
from .models import User
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from .forms import UserCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserProfileForm, UserAccessUpdateForm, UserCreateAccessForm
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import get_object_or_404
from core.utils import generate_random_number
from django.http import JsonResponse

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


# ###############Access Management
def accessmanagement(request):
    return render(request, 'accounts/access_management.html')


class UserListView(ListView):
    model = User
    template_name = 'accounts/access_user_list.html'
    context_object_name = 'users'


class UserTeacherListView(ListView):
    model = User
    template_name = 'accounts/access_user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(user_type='T')
    
class UserStaffListView(ListView):
    model = User
    template_name = 'accounts/access_user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(user_type='STA')


class UserDetailView(DetailView):
    model = User
    template_name = 'accounts/access_user_detail.html'
    context_object_name = 'user'
    slug_url_kwarg = 'user_id'    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(User, id=user_id)


class TeacherRegisterView(CreateView):    
    template_name = 'accounts/access_user_register.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 'T'                            
        user = form.save()
        return HttpResponseRedirect(reverse('access-user-teacher'))


class StaffRegisterView(CreateView):
    template_name = 'accounts/access_user_register.html'
    form_class = UserCreateForm    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 'STA'
        user = form.save()
        return HttpResponseRedirect(reverse('access-user-staff'))        
    
    

class UserProfileUpdateView(UpdateView):
    model = Profile
    form_class = UserProfileForm
    template_name = 'accounts/access_user_profile_update.html'    
   
    def get_success_url(self):
        user_id = self.object.user.id
        return reverse('access-user-detail', kwargs={'user_id': user_id})

    def form_valid(self, form):
        form.user = self.object.user
        print(form.cleaned_data)
        print(self.object)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(self.object)
        print(form.errors)        
        return super().form_invalid(form)    

    def get_object(self):
        user_id = self.kwargs['user_id']
        try:
            return Profile.objects.get(id=user_id)
        except Profile.DoesNotExist:
            raise Http404("User not found")
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(id=self.kwargs['user_id'])
        return context
    


class UserCreateAccessView(UpdateView):
    model = User
    form_class = UserCreateAccessForm
    template_name = 'accounts/access_user_access.html'

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
    template_name = 'accounts/access_user_access_update.html'

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
    
        


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'accounts/access_user_confirm_delete.html'
    success_url = reverse_lazy('access-user-list')  # Redirect after successful deletion

    def get_object(self):
        user_id = self.kwargs.get("user_id")  # Retrieve 'user_id' from URL
        return User.objects.get(id=user_id)

    def test_func(self):
        return self.request.user.is_superuser  # Only SuperAdmin can delete users
    

### Group Views
class GroupListView(ListView):
    model = Group
    template_name = 'accounts/access_group_list.html'
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
    template_name = 'accounts/access_group_form.html'
    fields = ['name', 'permissions']
    success_url = reverse_lazy('access-group-list')

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'accounts/access_group_form.html'
    fields = ['name', 'permissions']
    success_url = reverse_lazy('access-group-list')

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'accounts/access_group_confirm_delete.html'
    success_url = reverse_lazy('access-group-list')  # Redirect after successful deletion

    def get_object(self):
        group_id = self.kwargs.get("pk")  # Retrieve 'user_id' from URL
        return Group.objects.get(id=group_id)

    def test_func(self):
        return self.request.user.is_superuser  # Only SuperAdmin can delete users
    




# ########## Teacher Views
# # List all Teacher (Read - List)
# class TeacherListView(ListView):
#     model = User
#     template_name = 'core/teacher_list.html'  # Template to render the list of students
#     context_object_name = 'teachers'
#     paginate_by = 10

#     def get_queryset(self):
#         teacher = User.objects.filter(acc_type='TS')
#         if  self.request.GET:
#             teacher_query = self.request.GET.get('search')
#             if teacher_query:
#                 teacher = teacher.filter(first_name__icontains=teacher_query) or teacher.filter(last_name__icontains=teacher_query)
#         return teacher
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['total_teacher'] = User.objects.filter(acc_type='TS').count()
#         return context


# class TeacherDetailView(DetailView):
#     model = User
#     template_name = 'core/teacher_detail.html'
#     context_object_name = 'teacher'
#     slug_url_kwarg = 'acc_id'
#     slug_field = 'acc_id'


# # # Update an existing Teacher (Update)
# # class TeacherUpdateView(UpdateView):
# #     model = User
# #     template_name = 'core/teacher_form.html'  # Reusing the form template for editing
# #     form_class = UserProfileForm
# #     slug_url_kwarg = 'acc_id'
# #     slug_field = 'acc_id'
# #     success_url = reverse_lazy('teacher-list')  # Redirect to the Teaher list view on success


# ########## Staff Views
# # List all Teacher (Read - List)
# class StaffListView(ListView):
#     model = User
#     template_name = 'core/staff_list.html'  # Template to render the list of students
#     context_object_name = 'staffs'
#     paginate_by = 10

#     def get_queryset(self):
#         teacher = User.objects.filter(acc_type='NT')
#         if  self.request.GET:
#             teacher_query = self.request.GET.get('search')
#             if teacher_query:
#                 teacher = teacher.filter(first_name__icontains=teacher_query) or teacher.filter(last_name__icontains=teacher_query)
#         return teacher
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['total_staff'] = User.objects.filter(acc_type='NT').count()
#         return context
    
# class StaffDetailView(DetailView):
#     model = User
#     template_name = 'core/staff_detail.html'
#     context_object_name = 'staff'
#     slug_url_kwarg = 'acc_id'

#     def get_object(self):
#         acc_id = self.kwargs.get('acc_id')
#         return get_object_or_404(User, acc_id=acc_id)


# # # Update an existing Teacher (Update)
# # class StaffUpdateView(UpdateView):
# #     model = User
# #     template_name = 'core/staff_form.html'  # Reusing the form template for editing
# #     form_class = UserProfileForm
# #     slug_url_kwarg = 'acc_id'
# #     slug_field = 'acc_id'
# #     success_url = reverse_lazy('staff-list')  # Redirect to the Teaher list view on success