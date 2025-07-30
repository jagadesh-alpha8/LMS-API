from django.http import HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont
import io
import json
import os

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def generate_certificate(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)
        name = data.get('name')
        course = data.get('course')

        if not name or not course:
            return JsonResponse({'error': 'Missing name or course'}, status=400)

        # Static paths
        template_path = os.path.join(settings.BASE_DIR, 'static', 'certificate_template.png')
        font_path = os.path.join(settings.BASE_DIR, 'static', 'arial.ttf')

        # Load image and font
        certificate = Image.open(template_path).convert("RGB")  # RGB required for PDF
        draw = ImageDraw.Draw(certificate)
        font = ImageFont.truetype(font_path, size=40)

        # Update coordinates to match underline positions
        name_center_x, name_center_y = 1000, 650
        course_center_x, course_center_y = 1000, 750

        # Measure text
        name_bbox = draw.textbbox((0, 0), name, font=font)
        name_width = name_bbox[2] - name_bbox[0]
        name_height = name_bbox[3] - name_bbox[1]

        course_bbox = draw.textbbox((0, 0), course, font=font)
        course_width = course_bbox[2] - course_bbox[0]
        course_height = course_bbox[3] - course_bbox[1]

        # Calculate positions
        name_position = (name_center_x - name_width / 2, name_center_y - name_height / 2)
        course_position = (course_center_x - course_width / 2, course_center_y - course_height / 2)

        # Draw text
        draw.text(name_position, name, fill="black", font=font)
        draw.text(course_position, course, fill="black", font=font)

        # Save as PDF to buffer
        pdf_buffer = io.BytesIO()
        certificate.save(pdf_buffer, "PDF", resolution=100.0)
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
