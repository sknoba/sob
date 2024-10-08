from django.db import models
from core.models import Student
from django.dispatch import receiver
from django.db.models.signals import post_save


class FeesCollection(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('unpaid', 'Unpaid'),
    )

    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_fees = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
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
        return f"{self.student} - {self.payment_status}"

class Invoice(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.invoice_no} - {self.student}"

@receiver(post_save, sender=Invoice)
def update_fees_collection(sender, instance, created, **kwargs):
    if created:
        fees_collection = FeesCollection.objects.get(student=instance.student)
        fees_collection.paid_fees += instance.amount_paid
        fees_collection.save()
