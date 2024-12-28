# from django.contrib import admin
# from .models import FeesCollection

# @admin.register(FeesCollection)
# class FeesCollectionAdmin(admin.ModelAdmin):
#     list_display = ('enrollment', 'total_fees', 'paid_fees', 'remaining_fees', 'payment_status', 'due_date')
#     list_filter = ('payment_status', 'due_date')
#     search_fields = ('enrollment__student__first_name', 'enrollment__student__last_name', 'enrollment__student__student_id')
#     readonly_fields = ('paid_fees', 'remaining_fees', 'payment_status')


#     def get_readonly_fields(self, request, obj=None):
#         if obj:  # editing an existing object
#             return self.readonly_fields + ('enrollment', 'total_fees',)
#         return self.readonly_fields
    
#     def get_inline_instances(self, request, obj=None):
#         inline_instances = super().get_inline_instances(request, obj)
#         for inline in inline_instances:
#             # Set the parent object for filtering
#             inline.parent_object = obj
#         return inline_instances
    

# @admin.register(Invoice)
# class InvoiceAdmin(admin.ModelAdmin):
#     list_display = ('invoice_no', 'fees_collection', 'date', 'amount_paid', 'payment_method')
#     list_filter = ('payment_method', 'date')
#     search_fields = ('invoice_no', 'fees_collection__student__first_name', 'fees_collection__student__last_name', 'fees_collection__student__student_id')
#     readonly_fields = ('invoice_no',)

#     def student_link(self, obj):
#         if obj.student:
#             return f'<a href="/admin/yourapp/student/{obj.student.id}/change/">{obj.student}</a>'
#         return "No Student"
    
#     student_link.allow_tags = True  # Allow HTML rendering in admin
#     student_link.short_description = 'Student'


# from django.contrib import admin
# from .models import FeesStructure, FeesCollection, Invoice

# @admin.register(FeesStructure)
# class FeesStructureAdmin(admin.ModelAdmin):
#     list_display = ('class_name', 'academic_year', 'school_fees', 'uniform_fees', 'admission_fees')

# @admin.register(FeesCollection)
# class FeesCollectionAdmin(admin.ModelAdmin):
#     list_display = ('student_name', 'fees_structure', 'collected_date', 'total_fees')

# @admin.register(Invoice)
# class InvoiceAdmin(admin.ModelAdmin):
#     list_display = ('fees_collection', 'generated_date', 'total_fees')


# from django.contrib import admin
# from .models import FeesStructure, TransportFees, FeesCollection

# @admin.register(FeesStructure)
# class FeesStructureAdmin(admin.ModelAdmin):
#     list_display = ('class_name', 'academic_year', 'school_fee')
#     search_fields = ('class_name__name', 'academic_year__name')
#     list_filter = ('academic_year',)
#     ordering = ('class_name', 'academic_year')

# @admin.register(TransportFees)
# class TransportFeesAdmin(admin.ModelAdmin):
#     list_display = ('bus_route', 'academic_year', 'transport_fee')
#     search_fields = ('bus_route', 'academic_year__name')
#     list_filter = ('academic_year',)
#     ordering = ('bus_route', 'academic_year')

# @admin.register(FeesCollection)
# class FeesCollectionAdmin(admin.ModelAdmin):
#     list_display = (
#         'enrollment', 'fees_structure', 'transport', 'payment_status', 
#         'school_fee_concession', 'transport_fee_concession', 'remaning_amount', 'paid_fees'
#     )
#     search_fields = (
#         'enrollment__student__first_name', 'enrollment__student__last_name', 
#         'fees_structure__class_name__name', 'fees_structure__academic_year__name',
#         'transport__bus_route'
#     )
#     list_filter = ('payment_status', 'fees_structure__academic_year')
#     ordering = ('enrollment', 'fees_structure')
#     readonly_fields = ('total_fees',)