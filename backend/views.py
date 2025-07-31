from django.http import HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont
import io
import json
import os
from courses.models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def generate_certificate(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)
        name = data.get('name', '').title()  # Capitalize each word
        course = data.get('course').title()
        college = data.get('college')
        month = data.get('month')

        if not all([name, course, college, month]):
            return JsonResponse({'error': 'Missing name, course, college, or month'}, status=400)

        try:
            user = User.objects.get(first_name__iexact=name.split()[0])
            course = Course.objects.get(name__iexact=name)
            Subscription.objects.filter(user=user, course=course).update(certificate_issued=True)
        except (User.DoesNotExist, Course.DoesNotExist):
            pass  # Don't block certificate creation if user not matched
        
        # Paths
        template_path = os.path.join(settings.BASE_DIR, 'static', 'certificate.png')
        font_alexbrush = os.path.join(settings.BASE_DIR, 'static', 'AlexBrush-Regula for Name 23pt.ttf')
        font_rubik = os.path.join(settings.BASE_DIR, 'static', 'Rubik-Medium Course Name 14pt.ttf')
        font_montserrat = os.path.join(settings.BASE_DIR, 'static', 'Montserrat-Medium for College Name 13pt.ttf')

        # Load image and fonts
        certificate = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(certificate)

        font_name = ImageFont.truetype(font_alexbrush, size=200)
        font_course = ImageFont.truetype(font_rubik, size=53)
        font_college = ImageFont.truetype(font_montserrat, size=48)
        font_month = ImageFont.truetype(font_montserrat, size=48)  # Not bold

        # Coordinates
        name_center = (1754, 1220)
        course_center = (1754, 1670)
        college_center = (1754, 1480)
        month_center = (849, 2096)

        # Draw text centered
        def draw_centered_text(text, center, font, fill="black"):
            bbox = draw.textbbox((0, 0), text, font=font)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            position = (center[0] - width / 2, center[1] - height / 2)
            draw.text(position, text, font=font, fill=fill)

        # Draw all fields
        draw_centered_text(name, name_center, font_name, fill="#104784")
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
