
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from .models import FeesCollection, FeesStructure ,Invoince, TransportFees
from core.models import AcademicYear, Class
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import FormView
from django.views import View
from django.urls import reverse, reverse_lazy
from .forms import *
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect

from django.db.models import ProtectedError
from django.contrib import messages


from django.db.models.deletion import Collector
from django.db import DEFAULT_DB_ALIAS
from django.db import models


class FeesDashboardView(ListView):
    model = Invoince
    template_name = 'school_fees/dashboard.html'
    context_object_name = 'invoinces'


class FeesStructureView(FormView):
    model = FeesStructure
    template_name = 'school_fees/fees_structure_list.html'  # Template to render the list of students
    form_class = FeesStructureForm
    success_url = '/fees/fees-structures/'  # Redirect to the list view


    def form_valid(self, form):
        print('this is form valid')
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print('this is form invalid')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feesstructures'] = FeesStructure.objects.all().order_by('-id')
        return context
    
class FeesStructureCreateView(View):
    def get(self, request):
        classes = Class.objects.all()
        academic_years = AcademicYear.objects.all()
        form = FeesStructureForm()
        return render(request, 'fees_structure_form.html', {
            'form': form,
            'classes': classes,
        })
    
    def post(self, request):
        form = FeesStructureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fees_structure_list')  # Redirect to the list view
        else:
            classes = Class.objects.all()
            academic_years = AcademicYear.objects.all()
            return render(request, 'fees_structure_form.html', {
                'form': form,
                'classes': classes,
                'academic_years': academic_years
            })
        

class FeesStuctureDeleteView(DeleteView):
    model = FeesStructure
    template_name = 'school_fees/fees_structure_delete.html'
    success_url = reverse_lazy('fees-structure-list')  # Redirect after successful deletion

    def get_object(self):
        fee_structure_id = self.kwargs.get("fee_struc_id")  # Retrieve 'user_id' from URL
        return FeesStructure.objects.get(id=fee_structure_id)
    


class TransportFeesView(CreateView):
    model = TransportFees
    template_name = 'school_fees/tranport_fees_list.html'  # Template to render the list of students
    form_class = TranportFeesForm
    success_url = '/fees/fees-tranports/'  # Redirect to the list view

    def form_valid(self, form):        
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):        
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busroutes'] = TransportFees.objects.all().order_by('-id')
        return context































class FeesCollectionListView(ListView):
    model = FeesCollection
    template_name = 'school_fees/fees_collection_list.html'  # Template to render the list of students
    context_object_name = 'feescollection'  


    
    # def get_queryset(self):
    #     students = Student.objects.all()
    #     if  self.request.GET:
    #         select_class = self.request.GET.get('class')
    #         if select_class and select_class != 'no-class':
    #             students = students.filter(standard__id__icontains=select_class)
    #     return students.order_by('id')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academic_years'] = AcademicYear.objects.filter(is_active=True)
        return context
    

class FeesCollectionDetailView(DetailView):
    model = FeesCollection
    template_name = 'school_fees/fees_collection_detail.html'
    context_object_name = 'feescollection'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_invoince'] = Invoince.objects.filter(fees_collection=self.object).count()
        return context

def get_invoice_details(request, pk):
        invoice = get_object_or_404(Invoince, pk=pk)
        print('this is sec')
        data = {
            'registration_no' : invoice.fees_collection.enrollment.student.student_id,
            # 'roll_no': None,
            'name': invoice.fees_collection.enrollment.student.get_full_name(),
            # 'class': invoice.fees_collection.enrollment.student.standard.name or None,
            'total_fee': invoice.fees_collection.total_fees,
            'amount_paid': invoice.amount_paid,
            'total_paid_fee': invoice.fees_collection.paid_fees,
            'remaining_fees': invoice.fees_collection.remaining_fees,
            # 'fee_in_word': None,
            'receipt_date': invoice.date,
            'invoice_no' : invoice.invoice_no,
            'remark': invoice.remarks,
        }
        return JsonResponse(data)


class InvoiceCreateView(CreateView):
    model = Invoince
    form_class = InvoiceForm
    template_name = 'school_fees/invoince_create.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('fees-detail', kwargs={'pk': self.kwargs.get('pk')})
    
    def form_valid(self, form):
        form.instance.fees_collection = FeesCollection.objects.get(id=self.kwargs.get('pk'))
        form.save()
        response_data = {
            'message': 'Invoince Created Successfully',
            'status': 'success',
        }
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fees_collection'] = FeesCollection.objects.get(id=self.kwargs.get('pk'))
        context['date'] = timezone.datetime.now()
        return context


# views.py


def get_transport_fee(request):
    # Get parameters from the AJAX request
    bus_route = request.GET.get('bus_route')    
    print('this is bus_route', bus_route)    

    if bus_route:
        try:
            # Fetch the transport fee for the specific bus route and academic year
            transport_fee_obj = TransportFees.objects.get(
                id=bus_route,
            )
            # Return the transport fee in JSON format
            return JsonResponse({
                'transport_fee': str(transport_fee_obj.transport_fee),  # Convert decimal to string

            })

        except TransportFees.DoesNotExist:
            return JsonResponse({'error': 'Transport fee not found for the selected route'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)
