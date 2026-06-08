from django.conf import settings
from django.core.management.base import BaseCommand
from creditapp.template_builder import ensure_templates


class Command(BaseCommand):
    help = 'Создать .docx-шаблоны документов'

    def handle(self, *args, **options):
        ensure_templates(settings.DOCX_TEMPLATES_DIR)
        self.stdout.write(self.style.SUCCESS(f'Шаблоны созданы в {settings.DOCX_TEMPLATES_DIR}'))
# можно еще вот так но так по инету говорят по круче 
# self.stdout.write(self.style.SUCCESS('Шаблоны созданы в ' + str(settings.DOCX_TEMPLATES_DIR)))"