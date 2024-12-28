# from django.db import models
# from student.models import Student, Enrollment
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.utils import timezone


# class FeesCollection(models.Model):
#     PAYMENT_STATUS_CHOICES = (
#         ('paid', 'Paid'),
#         ('partially_paid', 'Partially Paid'),
#         ('unpaid', 'Unpaid'),
#     )

#     enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='fees_collections')
#     total_fees = models.PositiveIntegerField()
#     paid_fees = models.PositiveIntegerField(default=0)
#     remaining_fees = models.PositiveIntegerField()
#     due_date = models.DateField(null=True, blank=True)
#     payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    
#     def save(self, *args, **kwargs):
#         self.remaining_fees = self.total_fees - self.paid_fees
#         if self.paid_fees >= self.total_fees:
#             self.payment_status = 'paid'
#         elif self.paid_fees > 0:
#             self.payment_status = 'partially_paid'
#         else:
#             self.payment_status = 'unpaid'
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.enrollment.student} - {self.payment_status}"

# class Invoice(models.Model):
#     PAYMENT_METHOD_CHOICES = (
#         ('cash', 'Cash'),
#         ('card', 'Card'),
#         ('online', 'Online'),
#     )

#     fees_collection = models.ForeignKey(FeesCollection, on_delete=models.CASCADE, related_name='invoices')
#     invoice_no = models.CharField(max_length=50, unique=True, auto_created=True)
#     date = models.DateTimeField(auto_now=True)
#     amount_paid = models.PositiveIntegerField()
#     payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
#     remarks = models.TextField(blank=True, null=True)

#     def save(self, *args, **kwargs):
#         if not self.invoice_no:
#             self.invoice_no = self.generate_invoice_no()
#         super().save(*args, **kwargs)

#     @staticmethod
#     def generate_invoice_no():
#         last_invoice = Invoice.objects.order_by('-id').first()
#         if last_invoice and last_invoice.invoice_no.startswith("INV"):
#             try:
#                 # Extract the numeric part from the last invoice (after "INV")
#                 last_number = int(last_invoice.invoice_no[3:])
#                 # Generate the next invoice number
#                 new_number = last_number + 1
#             except ValueError:
#                 # Fallback in case of unexpected invoice_no format
#                 new_number = 1
#         else:
#             # If no previous invoice exists or invoice_no is incorrectly formatted
#             new_number = 1

#         # Return the new invoice number formatted with leading zeros
#         return f"INV{new_number:06d}"

#     def __str__(self):
#         return f"Invoice {self.invoice_no} - {self.fees_collection.enrollment.student}"

# @receiver(post_save, sender=Invoice)
# def update_fees_collection(sender, instance, created, **kwargs):
#     if created:
#         fees_collection = instance.fees_collection
#         fees_collection.paid_fees += instance.amount_paid
#         fees_collection.save()


# from django.db import models


# # Fees Structure Model
# class FeesStructure(models.Model):
#     CLASS_CHOICES = [
#         ('Nursery', 'Nursery'),
#         ('KG', 'Kindergarten'),
#         ('1', 'Class 1'),
#         ('2', 'Class 2'),
#         # Add more classes as needed
#     ]

#     class_name = models.CharField(max_length=20, choices=CLASS_CHOICES)
#     academic_year = models.CharField(max_length=9)  # Example: "2023-2024"
#     school_fees = models.DecimalField(max_digits=10, decimal_places=2)
#     uniform_fees = models.DecimalField(max_digits=10, decimal_places=2)
#     admission_fees = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.class_name} ({self.academic_year})"


# # Fees Collection Model
# class FeesCollection(models.Model):
#     fees_structure = models.ForeignKey(FeesStructure, on_delete=models.CASCADE)
#     student_name = models.CharField(max_length=200)
#     school_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     uniform_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     admission_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     transport_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     other_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     collected_date = models.DateField(auto_now_add=True)

#     def total_fees(self):
#         return (
#             self.school_fees
#             + self.uniform_fees
#             + self.admission_fees
#             + self.transport_fees
#             + self.other_fees
#         )

#     def __str__(self):
#         return f"{self.student_name} - {self.fees_structure}"


# # Invoice Model
# class Invoice(models.Model):
#     fees_collection = models.ForeignKey(FeesCollection, on_delete=models.CASCADE, related_name="invoices")
#     school_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     uniform_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     admission_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     transport_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     other_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     generated_date = models.DateField(auto_now_add=True)

#     def total_fees(self):
#         return (
#             self.school_fees
#             + self.uniform_fees
#             + self.admission_fees
#             + self.transport_fees
#             + self.other_fees
#         )

#     def __str__(self):
#         return f"Invoice for {self.fees_collection.student_name} - {self.generated_date}"














# from django.db import models
# from core.models import Class, AcademicYear
# from student.models import Enrollment
# from simple_history.models import HistoricalRecords

# class FeesStructure(models.Model):    
#     class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='fees_structure', null=True, blank=True)    
#     academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='fees_structure')
#     school_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     history = HistoricalRecords()

#     class Meta:
#         unique_together = ('class_name', 'academic_year')

#     def __str__(self):
#         return self.class_name.name + ' ' + self.academic_year.name
    
# class TransportFees(models.Model):    
#     academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='bus_fees')
#     bus_route = models.CharField(max_length=100)
#     transport_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     history = HistoricalRecords()

#     def __str__(self):
#         return self.bus_route + ' ' + self.academic_year.name


# class FeesCollection(models.Model):
#     PAYMENT_STATUS_CHOICES = (
#         ('paid', 'Paid'),
#         ('partially_paid', 'Partially Paid'),
#         ('unpaid', 'Unpaid'),
#     )
#     enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='fees_collection')
#     fees_structure = models.ForeignKey(FeesStructure, on_delete=models.CASCADE, related_name='fees_collection')
#     transport = models.ForeignKey(TransportFees, on_delete=models.CASCADE, related_name='fees_collection', null=True, blank=True)
#     school_fee_concession = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     transport_fee_concession = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
#     # total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     remaning_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     paid_fees = models.DecimalField(max_digits=10, decimal_places=2)
#     history = HistoricalRecords()

#     def total_fees(self):
#         return (
#             (self.fees_structure.school_fee - self.school_fee_concession) 
#             + (self.transport.transport_fee - self.transport_fee_concession)
#         )

#     def __str__(self):
#         return self.enrollment.student.first_name + ' ' + self.enrollment.student.last_name






    
# class Invoince(models.Model):
#     PAYMENT_METHOD_CHOICES = (
#         ('cash', 'Cash'),
#         ('card', 'Card'),
#         ('online', 'Online'),
#     )
#     fees_collection = models.ForeignKey(FeesCollection, on_delete=models.CASCADE, related_name='invoice')
#     created_at = models.DateTimeField(auto_now_add=True)
#     school_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     admission_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     uniform_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     transport_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     other_fee_ammount1 = models.DecimalField(max_digits=10, decimal_places=2)
#     other_fee_ammount2 = models.DecimalField(max_digits=10, decimal_places=2)
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    
#     def __str__(self):
#         return self.fees_collection.enrollment.student.first_name + ' ' + self.fees_collection.enrollment.student.last_name