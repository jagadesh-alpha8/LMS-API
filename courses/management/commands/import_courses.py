import os
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from courses.models import Course, Module, Video

class Command(BaseCommand):
    help = 'Import course, module, and video data from Excel'

    def handle(self, *args, **kwargs):
        excel_path = os.path.join(settings.BASE_DIR, 'courses', 'data', 'data.xlsx')

        # Clear old data
        Video.objects.all().delete()
        Module.objects.all().delete()
        Course.objects.all().delete()

        # Load sheets
        df_courses = pd.read_excel(excel_path, sheet_name='courses')
        df_modules = pd.read_excel(excel_path, sheet_name='modules')
        df_videos = pd.read_excel(excel_path, sheet_name='videos')

        # Insert data
        for _, row in df_courses.iterrows():
            Course.objects.create(id=row['id'], name=row['name'], description=row['description'])

        for _, row in df_modules.iterrows():
            Module.objects.create(id=row['id'], course_id=row['course_id'], title=row['title'])


        for _, row in df_videos.iterrows():
            Video.objects.create(
                id=row['id'],
                course_id=row['course_id'],
                module_id=row['module_id'],
                title=row['title'],
                url=row['url']
            )

        self.stdout.write(self.style.SUCCESS("✅ Excel data imported successfully"))
