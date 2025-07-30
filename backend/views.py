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
        college = data.get('college')
        month = data.get('month')

        # Validate inputs
        if not all([name, course, college, month]):
            return JsonResponse({'error': 'Missing name, course, college, or month'}, status=400)

        # File paths to template and fonts
        template_path = os.path.join(settings.BASE_DIR, 'static', 'certificate.png')
        font_alexbrush = os.path.join(settings.BASE_DIR, 'static', 'AlexBrush-Regula for Name 23pt.ttf')
        font_rubik = os.path.join(settings.BASE_DIR, 'static', 'Rubik-Medium Course Name 14pt.ttf')
        font_montserrat = os.path.join(settings.BASE_DIR, 'static', 'Montserrat-Medium for College Name 13pt.ttf')

        # Load template image and create draw context
        certificate = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(certificate)

        # Load fonts with specified sizes
        font_name = ImageFont.truetype(font_alexbrush, size=80)
        font_course = ImageFont.truetype(font_rubik, size=53)
        font_college = ImageFont.truetype(font_montserrat, size=48)
        font_month = ImageFont.truetype(font_montserrat, size=48)

        # Center coordinates (adjust as per your template design)
        name_center = (1754, 1276)
        course_center = (1754, 1677)
        college_center = (1754, 1499)
        month_center = (849, 2096)

        # Draw text centered
        def draw_centered_text(text, center, font, fill="black"):
            bbox = draw.textbbox((0, 0), text, font=font)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            position = (center[0] - width / 2, center[1] - height / 2)
            draw.text(position, text, font=font, fill=fill)

        # Draw each field
        draw_centered_text(name, name_center, font_name)
        draw_centered_text(course, course_center, font_course)
        draw_centered_text(college, college_center, font_college)
        draw_centered_text(month, month_center, font_month)

        # Save to PDF
        pdf_buffer = io.BytesIO()
        certificate.save(pdf_buffer, "PDF", resolution=100.0)
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
