import shutil
import uuid
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .doc_generator import create_zip_archive, generate_documents
from .validators import validate_form_data

# запросы от фронта 
def index(request):
    return render(request, 'creditapp/index.html')


@require_POST
def generate_documents_view(request):
    data = {key: request.POST.get(key, '').strip() for key in request.POST}
    errors = validate_form_data(data)
    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    session_id = str(uuid.uuid4())
    output_dir = Path(settings.GENERATED_DOCS_DIR) / session_id

    try:
        files = generate_documents(
            data,
            settings.DOCX_TEMPLATES_DIR,
            output_dir,
        )
        zip_buffer = create_zip_archive(files)
    except Exception as exc:
        if output_dir.exists():
            shutil.rmtree(output_dir, ignore_errors=True)
        return JsonResponse(
            {'success': False, 'errors': {'_form': f'Ошибка генерации документов: {exc}'}},
            status=500,
        )

    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    lastname = data.get('lastname', 'zaemshik')
    response['Content-Disposition'] = (
        f'attachment; filename="kreditnye_dokumenty_{lastname}.zip"'
    )

    shutil.rmtree(output_dir, ignore_errors=True)
    return response
