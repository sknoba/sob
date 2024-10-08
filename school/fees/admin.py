from django.contrib import admin
from .models import FeesCollection, Invoice

@admin.register(FeesCollection)
class FeesCollectionAdmin(admin.ModelAdmin):
    list_display = ('student', 'total_fees', 'paid_fees', 'remaining_fees', 'payment_status', 'due_date')
    list_filter = ('payment_status', 'due_date')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id')
    readonly_fields = ('paid_fees', 'remaining_fees', 'payment_status')


    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('student', 'total_fees')
        return self.readonly_fields
    
    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        for inline in inline_instances:
            # Set the parent object for filtering
            inline.parent_object = obj
        return inline_instances
    

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'student', 'date', 'amount_paid', 'payment_method')
    list_filter = ('payment_method', 'date')
    search_fields = ('invoice_no', 'student__first_name', 'student__last_name', 'student__student_id')
    readonly_fields = ('invoice_no',)

    def student_link(self, obj):
        if obj.student:
            return f'<a href="/admin/yourapp/student/{obj.student.id}/change/">{obj.student}</a>'
        return "No Student"
    
    student_link.allow_tags = True  # Allow HTML rendering in admin
    student_link.short_description = 'Student'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only for new invoices
            # Generate a unique invoice number (you might want to implement a more sophisticated method)
            last_invoice = Invoice.objects.order_by('-id').first()
            if last_invoice:
                last_number = int(last_invoice.invoice_no[3:])
                obj.invoice_no = f"INV{last_number + 1:06d}"
            else:
                obj.invoice_no = "INV000001"
        
        super().save_model(request, obj, form, change)
