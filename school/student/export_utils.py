import weasyprint
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.views import View
from student.models import Student, Enrollment
from django.conf import settings

class GenerateStudentPDF(View):
    def get(self, request, id, *args, **kwargs):
        try:
            enrollment = Enrollment.objects.get(id=id)
        except Enrollment.DoesNotExist:
            raise Http404("Student record not found")

        school_logo_url = request.build_absolute_uri(settings.STATIC_URL + "core/img/school-logo.png")
        student_photo_url = request.build_absolute_uri(enrollment.student.photo.url) if enrollment.student.photo else None

        # Render the template with the student data
        html_content = render_to_string("student/enrollment_form.html", {
            'student': enrollment,  # Pass the student record to the template
            'school_logo_url': school_logo_url,
            'student_photo_url': student_photo_url,  # Pass the
            
        })

        # Generate the PDF
        pdf = weasyprint.HTML(string=html_content).write_pdf()

        # Create an HTTP response with the PDF content
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f"inline; filename=student_{id}_report.pdf"
        return response
    

class AddmissionReciptPdf(View):
    def get(self, request, id, *args, **kwargs):
        # Get the student record by ID
        try:
            enrollment = Enrollment.objects.get(id=id)
        except Enrollment.DoesNotExist:
            raise Http404("Enrollment record not found")

        # Generate the full URL for the school logo
        school_logo_url = request.build_absolute_uri(settings.STATIC_URL + "core/img/school-logo.png")

        # Render the template with the student data and logo URL
        html_content = render_to_string("student/enrollment_admisison_recipt.html", {
            'enrollment': enrollment,
            'school_logo_url': school_logo_url,  # Pass the logo URL
        })

        # Generate the PDF
        pdf = weasyprint.HTML(string=html_content).write_pdf()

        # Create an HTTP response with the PDF content
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f"inline; filename=student_{id}_report.pdf"

        return response
    
