from django.contrib import admin
from .models import FeesStructure, TransportFees, FeesCollection, Invoince
from simple_history.admin import SimpleHistoryAdmin
from django.utils.html import format_html


@admin.register(FeesStructure)
class FeesStructureAdmin(SimpleHistoryAdmin):
    list_display = ('class_name', 'academic_year', 'school_fee','id')
    search_fields = ('class_name__name', 'academic_year__name')
    list_filter = ('academic_year',)
    ordering = ('class_name', 'academic_year')
    exclude = ('academic_year',)

@admin.register(TransportFees)
class TransportFeesAdmin(SimpleHistoryAdmin):
    list_display = ('bus_route', 'academic_year', 'transport_fee')
    search_fields = ('bus_route', 'academic_year__name')
    list_filter = ('academic_year',)
    ordering = ('bus_route', 'academic_year')
    exclude = ('academic_year',)

@admin.register(FeesCollection)
class FeesCollectionAdmin(SimpleHistoryAdmin):
    list_display = (
        'enrollment', 'payment_status', 'remaning_amount', 'total_paid_fees'
    )
    search_fields = (
        'enrollment__student__first_name', 'enrollment__student__last_name', 
        'fees_structure__class_name__name', 'fees_structure__academic_year__name',
        'transport__bus_route'
    )
    list_filter = ('payment_status', 'fees_structure__academic_year')
    ordering = ('enrollment', 'fees_structure')
    readonly_fields = ('total_fees', 'payment_status', 'remaning_amount', 'total_paid_fees', 'fees_structure','final_school_fee', 'final_transport_fee')
    fieldsets = (
        (None, {
            'fields': ('enrollment', 'fees_structure', 'transport')
        }),
        ('Concession', {
            'fields': ('school_fee_concession', 'transport_fee_concession')
        }),
        ('Final Fees Details', {
            'fields': ('final_school_fee','final_transport_fee','total_fees',)
        }),
        ('Payment Details', {
            'fields': ('payment_status', 'paid_school_fee','paid_transport_fee', 'total_paid_fees','remaning_amount')
        }),
    )    



class InvoiceAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    # Display relevant fields in the list view
    list_display = ('invoice_number','invoice_date', 'fees_collection', 'school_fee', 'transport_fee','payment_method', 'student_name')
    
    # Make 'invoice_date' sortable in the list view
    list_filter = ('invoice_date', 'payment_method', 'fees_collection__payment_status')
    
    # Make 'payment_status' a read-only field
    readonly_fields = ('total_amount',)
    exclude = ('invoice_number',)

    # Search functionality
    search_fields = ('fees_collection__enrollment__student__first_name', 'fees_collection__enrollment__student__last_name', 'fees_collection__payment_status')

    # Ordering of records in the list view (default order)
    ordering = ('-invoice_date',)


    # def has_delete_permission(self, request, obj=None):
    #     # Optionally, disable delete button completely
    #     return False
    
    # You can also create a custom method for 'student_name' to show the student's name in the list view
    def student_name(self, obj):
        return format_html(
            "{} {}".format(obj.fees_collection.enrollment.student.first_name, obj.fees_collection.enrollment.student.last_name)
        )
    student_name.admin_order_field = 'fees_collection__enrollment__student__first_name'  # Allow ordering by student name
    student_name.short_description = 'Student Name'

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
    
        # Example: Make 'academic_year' read-only when obj is not None (i.e., when it's being edited, not created)
        if obj:  # obj is None when creating a new object
            readonly_fields += ('fees_collection', 'school_fee', 'transport_fee', 'payment_method' )
        
        return readonly_fields

    # Inline forms or other customizations could be added if needed

# Register the model with the admin interface
admin.site.register(Invoince, InvoiceAdmin)