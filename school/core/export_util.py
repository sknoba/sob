# import openpyxl
# from openpyxl.styles import Alignment
# from django.http import HttpResponse
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.platypus import Spacer
# import sys

# from person.models import Person


# def export_to_excel(queryset, mo_no_status, filename, worksheet_title='Voters List', headers=None):

#     # Create an in-memory Excel workbook
#     wb = openpyxl.Workbook()
#     ws = wb.active
#     ws.title = worksheet_title

#     # Default headers if none provided
#     if headers is None:
#         headers = ['क्र.','वोटर न.', 'नाव', 'वय', 'लिंग', 'मोबाईल नंबर']

#     # Write header row
#     ws.append(headers)

#     # Center-align the header row
#     for col_num in range(1, len(headers) + 1):
#         cell = ws.cell(row=1, column=col_num)
#         cell.alignment = Alignment(horizontal='center', vertical='center')

#     # Write data rows based on the queryset
#     for index, person in enumerate(queryset, start=1):
#         if mo_no_status == '1':
#             mobile_number = person.mobile if person.mobile and person.mobile.strip() else 'N/A'
#         else:
#             mobile_number = 'N/A'
#         ws.append([index, person.vno, person.first_name, person.age, person.sex, mobile_number])
        

#     # Prepare the HttpResponse to send the file
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'

#     # Save the workbook to the response
#     wb.save(response)
#     return response






# def export_to_pdf(queryset, mo_no_status, filename, title=None, booth_info=None):
#     # Set up the HttpResponse with the appropriate content type
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename={filename}.pdf'

#     # Register the Mangal font
#     pdfmetrics.registerFont(TTFont('Mangal', 'static/font/Mangal.ttf'))

#     # Create a PDF document with reportlab
#     pdf = SimpleDocTemplate(response, pagesize=A4)
#     elements = []

#     # Define the styles for the document
#     styles = getSampleStyleSheet()
#     title_style = ParagraphStyle(name='Title', fontName='Mangal', fontSize=16, alignment=TA_CENTER)
#     normal_style = ParagraphStyle(name='Normal', fontName='Mangal', fontSize=12)
#     english_style = ParagraphStyle(name='English', fontName='Times-Roman', fontSize=12)

#     # Title and Booth information
#     title = f"मतदार यादी"


#     booth_info = f"बूथ : {booth_info}"

#     elements.append(Paragraph(title, title_style))
#     elements.append(Spacer(1, 12))
#     elements.append(Paragraph(booth_info, normal_style))
#     elements.append(Spacer(1, 12))

#     # Table data
#     data = [
#         [Paragraph('<b>क्र.</b>', normal_style),Paragraph('<b>आयडी</b>', normal_style), Paragraph('<b>नाव</b>', normal_style), 
#          Paragraph('<b>वय</b>', normal_style), Paragraph('<b>लिंग</b>', normal_style),
#          Paragraph('<b>मो.क्र.</b>', normal_style)]
#     ]


#     #Add Table Data

#     for count, person in enumerate(queryset, start=1):
#         if mo_no_status == '1':
#             mobile_no = person.mobile if person.mobile else 'Not Available'
#         else:
#             mobile_no='N/A'

#         data.append([
#             Paragraph(str(count), normal_style),
#             Paragraph(str(person.vno), normal_style),
#             Paragraph(person.first_name, normal_style),
#             Paragraph(str(person.age), normal_style),
#             Paragraph('पु' if person.sex == 'M' else 'स्त्री', normal_style),
#             Paragraph(str(mobile_no), english_style),
#         ])

#     # Create table with styling
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Mangal'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))

#     elements.append(table)

#     # Build the PDF document
#     pdf.build(elements)

#     return response




# import io
# from reportlab.lib.pagesizes import A3, landscape
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepInFrame
# from reportlab.lib.units import cm
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors  # Add this import
# from django.http import FileResponse
# from reportlab.lib.pagesizes import landscape, A3
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepInFrame
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import cm
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics




# # def print_labels(request):
# #     pdfmetrics.registerFont(TTFont('Mangal', 'static/font/Mangal.ttf'))

# #     buffer = io.BytesIO()
# #     doc = SimpleDocTemplate(buffer, pagesize=landscape(A3))
# #     story = []

# #     dispatch_list = Person.objects.filter(id=1)
# #     styles = getSampleStyleSheet()
# #     styleN = styles['Normal']
# #     styleN.fontName = 'Mangal'

# #     labels = []
# #     for dispatch in dispatch_list:
# #         label_text =f"""       
# #             <font face="Mangal"><p>नमस्कार {dispatch.first_name},</p></font>
# #             <p>मतदार ओळख पत्र: {dispatch.epic_no}</p>
# #             <p>मतदार क्र: {dispatch.vno}</p>
# #             <p>नाव: {dispatch.first_name}</p>
# #             <p>आडनाव: {dispatch.last_name}</p>
# #             <p>पत्ता: {dispatch.address}</p>
# #             <p>धन्यवाद.</p>
       
# #     """

# #         label = Paragraph(label_text, styleN)
# #         framed_label = KeepInFrame(6.5*cm, 3.2*cm, [label], hAlign='LEFT', vAlign='BOTTOM', fakeWidth=False)
# #         labels.append(framed_label)

# #     # Pad labels with empty frames to ensure there are always enough data to create a 4x5 table
# #     while len(labels) % 20 != 0:
# #         labels.append(KeepInFrame(6.5*cm, 3.2*cm, [Paragraph("", styleN)]))

# #     # Split labels into chunks of 20
# #     for i in range(0, len(labels), 20):
# #         chunk = labels[i:i+20]
# #         # Create a table for each chunk
# #         data = [chunk[n:n+4] for n in range(0, len(chunk), 4)]
# #         table = Table(data, colWidths=[7.5*cm]*4, rowHeights=[4*cm]*5, hAlign='CENTER', vAlign='MIDDLE')
# #         table.setStyle(TableStyle([
# #             ('BOX', (0, 0), (-1, -1), 1, colors.black),
# #             ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
# #         ]))
# #         story.append(table)
# #         story.append(Spacer(1, 0.5*cm))  # Add vertical spacing between tables

# #     doc.build(story)
# #     buffer.seek(0)
# #     return FileResponse(buffer, as_attachment=True, filename='labels.pdf')


# from weasyprint import HTML, CSS
# from django.http import HttpResponse



# from django.http import HttpResponse

# # def export_voter_card(person):
# #     sections = f"""
# #     <!-- Voter Information Section -->
# #     <div class="voter-info">
# #         <table class="voter-info-table">
# #             <tr>
# #                 <th>मतदान केंद्र</th>
# #                 <td colspan="5">{person.booth}</td>
# #             </tr>
# #             <tr>
# #                 <th>मतदार क्र.</th>
# #                 <td>{person.booth_no}</td>
# #                 <th>लिंग</th>
# #                 <td>{person.sex}</td>
# #                 <th>वय</th>
# #                 <td>{person.age}</td>
# #             </tr>
# #             <tr>
# #                 <th>मतदार</th>
# #                 <td colspan="5">{person.first_name}</td>
# #             </tr>
# #             <tr>
# #                 <th>पत्ता</th>
# #                 <td colspan="5">{person.address}</td>
# #             </tr>
# #         </table>
# #     </div>
# #     """

# #     html_content = f"""
# #     <html lang="mr">
# #     <head>
# #         <meta charset="UTF-8">
# #         <style>
# #             body {{
# #                 font-family: 'Mangal', sans-serif;
# #                 margin: 0;
# #                 padding: 0;
# #                 font-size: 10px; /* Adjusted font size for small page */
# #             }}
# #             .header {{
# #                 background-color: #f48024;
# #                 text-align: center;
# #                 padding: 5px; /* Reduced padding */
# #                 color: white;
# #             }}
# #             .voter-info {{
# #                 margin: 5px; /* Reduced margin */
# #                 padding: 5px; /* Reduced padding */
# #                 border: 1px solid black; /* Reduced border width */
# #                 width: 100%; /* Changed to 100% for full width */
# #                 box-sizing: border-box;
# #             }}
# #             .voter-info-table {{
# #                 width: 100%;
# #                 border-collapse: collapse;
# #                 font-size: 8px; /* Adjusted font size for table */
# #             }}
# #             .voter-info-table th, .voter-info-table td {{
# #                 border: 1px solid black;
# #                 padding: 2px; /* Reduced padding */
# #             }}
# #             .sheet-title {{
# #                 text-align: center;
# #                 font-size: 16px; /* Adjusted title size */
# #                 color: #333;
# #                 margin: 5px 0; /* Reduced margin */
# #             }}
# #         </style>
# #     </head>
# #     <body>
# #         <h2 class="sheet-title">मतदार कार्ड</h2>
# #         {sections}
# #     </body>
# #     </html>
# #     """

# #     # Convert HTML to image
# #     imgkit_options = {
# #         'format': 'png',
# #         'width': '350',  # Width in pixels
# #         'height': '250',  # Height in pixels
# #     }
    
# #     img_data = imgkit.from_string(html_content, False, options=imgkit_options)

# #     # Create HTTP response
# #     response = HttpResponse(img_data, content_type="image/png")
# #     response["Content-Disposition"] = 'inline; filename="voter_card.png"'
    
# #     return response




# from django.http import HttpResponse

# def export_voter_card(person):
#     sections = f"""
#     <!-- Voter Information Section -->
#     <div class="voter-info">
#         <table class="voter-info-table">
#             <tr>
#                 <th>मतदान केंद्र</th>
#                 <td colspan="5">{person.booth}</td>
#             </tr>
#             <tr>
#                 <th>मतदार क्र.</th>
#                 <td>{person.booth_no}</td>
#                 <th>लिंग</th>
#                 <td>{person.sex}</td>
#                 <th>वय</th>
#                 <td>{person.age}</td>
#             </tr>
#             <tr>
#                 <th>मतदार</th>
#                 <td colspan="5">{person.first_name}</td>
#             </tr>
#             <tr>
#                 <th>पत्ता</th>
#                 <td colspan="5">{person.address}</td>
#             </tr>
#         </table>
#     </div>
#     """

#     html_content = f"""
#         <html lang="mr">
#         <head>
#             <meta charset="UTF-8">
#             <style>
#                 body {{
#                     font-family: 'Mangal', sans-serif;
#                     margin: 0;
#                     padding: 0;
#                     font-size: 10px; /* Adjusted font size for small page */
#                 }}
#                 .header {{
#                     background-color: #f48024;
#                     text-align: center;
#                     padding: 5px; /* Reduced padding */
#                     color: white;
#                 }}
#                 .header img {{
#                     height: 30px; /* Adjusted image height */
#                     margin: 0 5px; /* Reduced margin */
#                 }}
#                 .candidate-name {{
#                     font-size: 16px; /* Adjusted font size */
#                     font-weight: bold;
#                     color: red;
#                 }}
#                 .voting-instructions {{
#                     font-size: 12px; /* Adjusted font size */
#                     color: blue;
#                     margin-top: 5px; /* Reduced margin */
#                 }}
#                 .voter-info {{
#                     margin: 5px; /* Reduced margin */
#                     padding: 5px; /* Reduced padding */
#                     border: 1px solid black; /* Reduced border width */
#                     width: 100%; /* Changed to 100% for full width */
#                     box-sizing: border-box;
#                 }}
#                 .voter-info-table {{
#                     width: 100%;
#                     border-collapse: collapse;
#                     font-size: 8px; /* Adjusted font size for table */
#                 }}
#                 .voter-info-table th, .voter-info-table td {{
#                     border: 1px solid black;
#                     padding: 2px; /* Reduced padding */
#                 }}
#                 .footer {{
#                     clear: both;
#                     margin-top: 10px; /* Reduced margin */
#                     text-align: center;
#                     font-size: 8px; /* Adjusted font size */
#                     color: gray;
#                 }}
#                 @page {{
#                     size: 7cm 3.5cm;
#                     margin: 0;
#                 }}
#                 .sheet-title {{
#                     text-align: center;
#                     font-size: 16px; /* Adjusted title size */
#                     color: #333;
#                     margin: 5px 0; /* Reduced margin */
#                 }}
#             </style>
#         </head>
#         <body>
#             <h2 class="sheet-title">मतदार कार्ड</h2>
#             {sections}
#         </body>
#         </html>
#     """
#     pdf_file = HTML(string=html_content).write_pdf()
#     from pdf2image import convert_from_bytes
#     images = convert_from_bytes(pdf_file)

#     image_io = io.BytesIO()
#     images[0].save(image_io, format='JPEG')
#     image_io.seek(0)
#     # Generate image from HTML
#     response = HttpResponse(image_io.getvalue(), content_type='image/jpeg')
#     response['Content-Disposition'] = 'inline; filename="voter_card.jpg"'
#     return response



# def export_voter_cards(querysets):
#     # querysets = Person.objects.filter(booth__booth_no=str(1))
#     # print(querysets)
#     sections = ""
#     for dispatch in querysets:
#         sections += f"""
#         <!-- Voter Information Section -->
#         <div class="voter-info">
#             <table class="voter-info-table">
#                 <tr>
#                     <th>मतदान केंद्र</th>
#                     <td colspan="5">{dispatch.booth}</td>
#                 </tr>
#                 <tr>
#                     <th>मतदार क्र.</th>
#                     <td>{dispatch.booth_no}</td>
#                     <th>लिंग</th>
#                     <td>{dispatch.sex}</td>
#                     <th>वय</th>
#                     <td>{dispatch.age}</td>
#                 </tr>
#                 <tr>
#                     <th>मतदार</th>
#                     <td colspan="5">{dispatch.first_name}</td>
#                 </tr>
#                 <tr>
#                     <th>पत्ता</th>
#                     <td colspan="5">{dispatch.address}</td>
#                 </tr>
#             </table>
#         </div>
#         """

#     html_content = f"""
#     <html lang="mr">
#     <head>
#         <meta charset="UTF-8">
#         <style>
#             body {{
#                 font-family: 'Mangal', sans-serif;
#                 margin: 0;
#                 padding: 0;
#                 font-size: 16px;
#             }}
#             .header {{
#                 background-color: #f48024;
#                 text-align: center;
#                 padding: 20px;
#                 color: white;
#             }}
#             .header img {{
#                 height: 50px;
#                 margin: 0 10px;
#             }}
#             .candidate-name {{
#                 font-size: 36px;
#                 font-weight: bold;
#                 color: red;
#             }}
#             .voting-instructions {{
#                 font-size: 20px;
#                 color: blue;
#                 margin-top: 10px;
#             }}
#             .voter-info {{
#                 margin: 10px;
#                 padding: 10px;
#                 border: 2px solid black;
#                 width: 31%;
#                 float: left;
#                 box-sizing: border-box;
#             }}
#             .voter-info-table {{
#                 width: 100%;
#                 border-collapse: collapse;
#             }}
#             .voter-info-table th, .voter-info-table td {{
#                 border: 1px solid black;
#                 padding: 5px;
#             }}
#             .footer {{
#                 clear: both;
#                 margin-top: 30px;
#                 text-align: center;
#                 font-size: 12px;
#                 color: gray;
#             }}
#             @page {{
#                 size: A3 landscape;
#                 margin: 0;
#             }}
#             .sheet-title{{
#                 text-align: center;
#                 font-size: 40px;
#                 color: #333;
#                 margin: 20px 0;
#             }}
#         </style>
#     </head>
#     <body>
#         <h2 class="sheet-title"> मतदार कार्ड</h2>
#         {sections}
#     </body>
#     </html>
#     """

#     # Generate PDF
#     response = HttpResponse(content_type="application/pdf")
#     response["Content-Disposition"] = 'inline; filename="labels.pdf"'
#     HTML(string=html_content).write_pdf(response)
#     return response



import weasyprint
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.views import View
from .models import Student

class GenerateStudentPDF(View):
    def get(self, request, id, *args, **kwargs):
        # Get the student record by ID
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            raise Http404("Student record not found")

        # Render the template with the student data
        html_content = render_to_string("core/student_pdf.html", {
            'student': student  # Pass the student record to the template
        })

        # Generate the PDF
        pdf = weasyprint.HTML(string=html_content).write_pdf()

        # Create an HTTP response with the PDF content
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f"inline; filename=student_{id}_report.pdf"

        return response
