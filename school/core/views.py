from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .models import Class, Subject, AcademicYear
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from .forms import AcademicYearForm, ClassCreateForm, ClassUpdateFrom, SubjectForm, current_academic_year
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin


def get_all_instances():
    from accounts.models import User  # Import inside the function
    return User.objects.all()


    
@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')


import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from accounts.models import WebPushSubscription
from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse
from pywebpush import webpush, WebPushException


def vapid_config_js(request):
    # Render the template with the VAPID public key
    response = render(request, 'core/vapid_config.js', {
        'VAPID_PUBLIC_KEY': settings.WEBPUSH_SETTINGS['VAPID_PUBLIC_KEY'],
    })
    # Set the correct content type for JavaScript
    response['Content-Type'] = 'application/javascript'
    return response

@csrf_exempt
def save_subscription(request):
    print("ok")
    if request.method == 'POST':        
        subscription_info = json.loads(request.body)
        WebPushSubscription.objects.update_or_create(
            user=request.user,
            defaults={'subscription_info': subscription_info}
        )
        return JsonResponse({'status': 'success'})
    
def send_push_notification(user, title, body, url=None):
    subscriptions = WebPushSubscription.objects.filter(user=user)
    payload = {"title": title, "body": body, "url": url}
    for subscription in subscriptions:
        try:
            webpush(
                subscription_info=subscription.subscription_info,
                data=json.dumps(payload),
                vapid_private_key=settings.WEBPUSH_SETTINGS['VAPID_PRIVATE_KEY'],
                vapid_claims={
                    "sub": "mailto:" + settings.WEBPUSH_SETTINGS['VAPID_ADMIN_EMAIL']
                }
            )
        except WebPushException as ex:
            print("WebPush error:", ex)



# ############### Standard Views
class ClassView(CreateView):
    model = Class
    template_name = 'core/class_list.html'  # Template to render the list of students
    form_class = ClassCreateForm
    success_url = reverse_lazy('classes-list')  # Redirect to the Teaher list view on success        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = Class.objects.all().order_by('-id')        
        return context


class StandardDetailView(DetailView):
    model = Class
    template_name = 'core/standard_detail.html'
    context_object_name = 'standard'    

class StandardUpdateView(UpdateView):
    model = Class
    template_name = 'core/class_form.html'  
    form_class = ClassUpdateFrom    

    def get_success_url(self):
        class_id = self.object.id
        return reverse('class-detail', kwargs={'pk': class_id})

    def get_form(self, form_class=None):
        from student.models import Enrollment
        form = super().get_form(form_class)
        class_instance = self.get_object()

        # Filter boys and girls for the class
        boys = Enrollment.objects.filter(
            academic_year=current_academic_year(),
            standard=class_instance,
            student__gender='male'  # Ensure `student` has `gender` field
        )
        girls = Enrollment.objects.filter(
            academic_year=current_academic_year(),
            standard=class_instance,
            student__gender='female'
        )
        
        # Assign the filtered QuerySets to the form fields
        form.fields['class_monitor_boy'].queryset = boys.filter()
        form.fields['class_monitor_girl'].queryset = girls  # Corrected typo here
        return form
    

# class StandardDeleteView(PermissionRequiredMixin, DeleteView):
#     model = Standard
#     template_name = 'standard_confirm_delete.html'  # Template to confirm deletion
#     success_url = reverse_lazy('standard-list')  # Redirect to the Standard list view on success
#     permission_required = 'core.delete_standard'
# ##### Academic Year Views


class AcademicYearView(CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'core/academic_year_list.html'
    success_url = reverse_lazy('academic-year-list')

    def form_valid(self, form):
        messages.success(self.request, "Academic year created successfully!")
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academic_years'] = AcademicYear.objects.all().order_by('-id')
        return context


class AcademicYearDetailView(DetailView):
    model = AcademicYear
    template_name = 'core/academic_year_detail.html'
    context_object_name = 'academic_year'


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
    

class SubjectView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'core/subject_list.html'
    success_url = reverse_lazy('subject-list')

    def form_valid(self, form):
        messages.success(self.request, "Subject created successfully!")
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all().order_by('name')
        return context
    
class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'core/subject_detail.html'
    context_object_name = 'subject'


# class SubjectDeleteView(DeleteView):
#     model = Subject
#     template_name = 'core/subject_confirm_delete.html'
#     success_url = reverse_lazy('subject-list')

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, "Subject deleted successfully!")
#         return super().delete(request, *args, **kwargs)


# class SubjectUpdateView(UpdateView):
#     model = Subject
#     form_class = SubjectForm
#     template_name = 'core/subject_form.html'
#     success_url = reverse_lazy('subject-list')

#     def form_valid(self, form):
#         messages.success(self.request, "Subject updated successfully!")
#         return super().form_valid(form)
    
