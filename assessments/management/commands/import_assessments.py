from django.core.management.base import BaseCommand
import pandas as pd
from assessments.models import Assessment, Question
from courses.models import Course

class Command(BaseCommand):
    help = 'Import assessments and questions from Excel'

    def handle(self, *args, **kwargs):
        try:
            file_path = 'assessments/import/updated_assessment_questions.xlsx'  # Change path as needed
            df = pd.read_excel(file_path)

            grouped = df.groupby(['Course Name', 'Assessment Title'])

            for (course_name, assessment_title), group in grouped:
                course = Course.objects.filter(name=course_name).first()
                if not course:
                    self.stdout.write(self.style.WARNING(f"Course '{course_name}' not found, skipping."))
                    continue

                assessment, created = Assessment.objects.get_or_create(
                    course=course,
                    title=assessment_title,
                    defaults={
                        'description': group['Assessment Description'].iloc[0],
                        'total_marks': group.shape[0]
                    }
                )

                for _, row in group.iterrows():
                    Question.objects.create(
                        assessment=assessment,
                        question_text=row["Question"],
                        option_a=row["Option A"],
                        option_b=row["Option B"],
                        option_c=row["Option C"],
                        option_d=row["Option D"],
                        correct_option=row["Correct Option"]
                    )

                self.stdout.write(self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} assessment: '{assessment_title}' with {group.shape[0]} questions"
                ))

            self.stdout.write(self.style.SUCCESS("✅ Import completed successfully."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error: {e}"))
