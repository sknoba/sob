from django.db import models
from core.models import Student
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class FeesCollection(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('unpaid', 'Unpaid'),
    )

    enrollment = models.OneToOneField('enrollment.Enrollment', on_delete=models.CASCADE, related_name='fees_collections')
    total_fees = models.PositiveIntegerField()
    paid_fees = models.PositiveIntegerField(default=0)
    remaining_fees = models.PositiveIntegerField()
    due_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    
    def save(self, *args, **kwargs):
        self.remaining_fees = self.total_fees - self.paid_fees
        if self.paid_fees >= self.total_fees:
            self.payment_status = 'paid'
        elif self.paid_fees > 0:
            self.payment_status = 'partially_paid'
        else:
            self.payment_status = 'unpaid'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enrollment.student} - {self.payment_status}"

class Invoice(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    )

    fees_collection = models.ForeignKey(FeesCollection, on_delete=models.CASCADE, related_name='invoices')
    invoice_no = models.CharField(max_length=50, unique=True, auto_created=True)
    date = models.DateTimeField(auto_now=True)
    amount_paid = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            self.invoice_no = self.generate_invoice_no()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_invoice_no():
        last_invoice = Invoice.objects.order_by('-id').first()
        if last_invoice and last_invoice.invoice_no.startswith("INV"):
            try:
                # Extract the numeric part from the last invoice (after "INV")
                last_number = int(last_invoice.invoice_no[3:])
                # Generate the next invoice number
                new_number = last_number + 1
            except ValueError:
                # Fallback in case of unexpected invoice_no format
                new_number = 1
        else:
            # If no previous invoice exists or invoice_no is incorrectly formatted
            new_number = 1

        # Return the new invoice number formatted with leading zeros
        return f"INV{new_number:06d}"

    def __str__(self):
        return f"Invoice {self.invoice_no} - {self.fees_collection.enrollment.student}"

@receiver(post_save, sender=Invoice)
def update_fees_collection(sender, instance, created, **kwargs):
    if created:
        fees_collection = instance.fees_collection
        fees_collection.paid_fees += instance.amount_paid
        fees_collection.save()


