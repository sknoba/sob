# import weasyprint
# from django.http import HttpResponse, Http404
# from django.template.loader import render_to_string
# from django.db.models import Sum
# from django.core.exceptions import ObjectDoesNotExist
# from django.views import View
# from .models import Invoice



# class GenerateInvoincePDF(View):
    
#     def get(self, request, id, *args, **kwargs):
#         # Get the student record by ID
#         try:
#             invoince = Invoice.objects.get(id=id)            
#             invoices_before=  Invoice.objects.filter(fees_collection=invoince.fees_collection).filter(date__lt=invoince.date)
#             total_amount_before = invoices_before.aggregate(Sum('amount_paid'))
#             if total_amount_before['amount_paid__sum'] is None:
#                 total_amount_before['amount_paid__sum'] = 0

#             remaning_amount = invoince.fees_collection.total_fees - total_amount_before['amount_paid__sum']
#             remaning_amount = remaning_amount - invoince.amount_paid
#         except Invoice.DoesNotExist:
#             raise Http404("Invoince record not found")
#         # Render the template with the student data
#         html_content = render_to_string("fees/invoince_pdf.html", {
#             'total_amount_before': total_amount_before,
#             'invoince': invoince,
#             'remaning_amount': remaning_amount,
#         })

#         # Generate the PDF
#         pdf = weasyprint.HTML(string=html_content).write_pdf()

#         # Create an HTTP response with the PDF content
#         response = HttpResponse(pdf, content_type="application/pdf")
#         file_name = Invoice.objects.get(id=id)
#         response["Content-Disposition"] = f"inline; filename={file_name.invoice_no}_{file_name.fees_collection.student.first_name}_{file_name.fees_collection.student.last_name}.pdf"

#         return response
    