from django.db import models
from core.models import Class, AcademicYear
from student.models import Enrollment
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from core.forms import current_academic_year

class FeesStructure(models.Model):    
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='fees_structure', verbose_name='Class')    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='fees_structure')
    school_fee = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name='School Fee')
    history = HistoricalRecords()

    class Meta:
        unique_together = ('class_name', 'academic_year')

    def save(self, *args, **kwargs):
        if not self.id:
            self.academic_year = current_academic_year()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.class_name.section:
            return f"{self.class_name.name} {self.class_name.section} {self.academic_year.name}"
        return f"{self.class_name.name} {self.academic_year.name}"
    
    
class TransportFees(models.Model):    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='bus_fees')
    bus_route = models.CharField(max_length=100, verbose_name='Bus Route')
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fare")
    history = HistoricalRecords()   

    def save(self, *args, **kwargs):
        if not self.id:
            self.academic_year = current_academic_year()
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.bus_route + ' ' + self.academic_year.name


class FeesCollection(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('complete_paid', 'Complete Paid'),
        ('partially_paid', 'Partially Paid'),
        ('unpaid', 'Unpaid'),
    )
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='fees_collection')
    fees_structure = models.ForeignKey(FeesStructure, on_delete=models.PROTECT, related_name='fees_collection')
    transport = models.ForeignKey(TransportFees, on_delete=models.CASCADE, related_name='fees_collection', null=True, blank=True)
    school_fee_concession = models.PositiveIntegerField(default=0)
    paid_school_fee = models.PositiveIntegerField(default=0)
    transport_fee_concession = models.PositiveIntegerField(default=0)    
    paid_transport_fee = models.PositiveIntegerField(default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    remaning_amount = models.PositiveIntegerField(default=0)
    total_paid_fees = models.PositiveIntegerField(default=0)
    history = HistoricalRecords()

    def final_school_fee(self):
        return self.fees_structure.school_fee - self.school_fee_concession if self.fees_structure else 0
    
    def final_transport_fee(self):
        return (self.transport.transport_fee if self.transport else 0) - (self.transport_fee_concession if self.transport else 0)
    
    def total_fees(self):
        school_fee = self.final_school_fee()
        transport_fee = self.final_transport_fee()
        return school_fee + transport_fee


    def clean(self):      
        # if not self.fees_structure:                        
        #     academic_year = self.enrollment.academic_year
        #     class_name = self.enrollment.standard
        #     try:
        #         self.fees_structure = FeesStructure.objects.get(academic_year=academic_year, class_name=class_name)
        #     except FeesStructure.DoesNotExist:
        #         raise ValidationError(
        #             f"FeesStructure for the class '{class_name}' is not available for the academic year '{academic_year}'."
        #         )
        # if self.paid_school_fee > self.final_school_fee():
        #     raise ValidationError(f"Paid school fee cannot exceed the final school fee of {self.final_school_fee()}.")

        # if self.paid_transport_fee > self.final_transport_fee():
        #     raise ValidationError(f"Paid transport fee cannot exceed the final transport fee of {self.final_transport_fee()}.")
        pass

    def save(self, *args, **kwargs):
        # Ensure remaining amount is calculated
        self.total_paid_fees = self.paid_school_fee + self.paid_transport_fee
        self.remaning_amount = self.total_fees() - self.total_paid_fees
        
        if self.total_paid_fees == self.total_fees():
            self.payment_status = 'complete_paid'
        elif self.total_paid_fees > 0:
            self.payment_status = 'partially_paid'
        else:
            self.payment_status = 'unpaid'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.enrollment.student.first_name + ' ' + self.enrollment.student.last_name + ' '  + self.payment_status 


class Invoince(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    )
    invoice_number = models.CharField(max_length=20, unique=True)
    fees_collection = models.ForeignKey(FeesCollection, on_delete=models.CASCADE, related_name='invoice')
    invoice_date = models.DateTimeField(auto_now_add=True)
    school_fee = models.PositiveIntegerField()
    transport_fee = models.PositiveIntegerField(default=0, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    canceled = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    history = HistoricalRecords()

    def generate_invoice_number(self):
        ay = self.fees_collection.enrollment.academic_year
        academic_prifix = str(ay.start_date.year)[-2:] + str(ay.end_date.year)[-2:]
        this_month_inv_count = Invoince.objects.filter(invoice_date__month=now().month).count()+1
        inv = academic_prifix + str(now().month) + str(this_month_inv_count)
        return f"INV-{inv}"

    def total_amount(self):
        if self.school_fee or self.transport_fee:
            return self.school_fee + self.transport_fee

    def clean(self):
        """Override clean to validate remaining fees before creating an invoice."""
        if not self.fees_collection:
            raise ValidationError("FeesCollection is required to create an invoice.")
        
        if self.fees_collection.remaning_amount <= 0:
            raise ValidationError(f"No remaining fees to pay for {self.fees_collection}. Invoice cannot be created.")        
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        fees_collection = self.fees_collection
        fees_collection.paid_school_fee += self.school_fee
        fees_collection.paid_transport_fee += self.transport_fee
        fees_collection.save()
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     """Override delete to prevent invoice deletion."""
    #     raise ValidationError("Invoice cannot be deleted once created.")
        
    def __str__(self):
        """Custom string representation."""
        return f"{self.fees_collection.enrollment.student.first_name} {self.fees_collection.enrollment.student.last_name} - {self.fees_collection.payment_status}"
    