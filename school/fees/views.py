from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from .models import FeesCollection, Invoice
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .forms import InvoiceForm
from django.http import JsonResponse
from django.utils import timezone


class FeesDashboardView(ListView):
    model = Invoice
    template_name = 'fees/dashboard.html'
    context_object_name = 'invoinces'
    ordering = ['-date']


class FeesCollectionListView(ListView):
    model = FeesCollection
    template_name = 'fees/fees_collection_list.html'  # Template to render the list of students
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
        context['total_fees_collection'] = FeesCollection.objects.count()
        return context
    

class FeesCollectionDetailView(DetailView):
    model = FeesCollection
    template_name = 'fees/fees_collection_detail.html'
    context_object_name = 'feescollection'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_invoince'] = Invoice.objects.filter(fees_collection=self.object).count()
        return context

def get_invoice_details(request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
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
    model = Invoice
    form_class = InvoiceForm
    template_name = 'fees/invoince_create.html'
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
    