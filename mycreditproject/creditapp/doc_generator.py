import io
import zipfile
from pathlib import Path

from .doc_filler import render_docx
from .formatters import build_context
from .scoring import calculate_scoring
from .template_builder import TEMPLATE_FILES, ensure_templates


def _enrich_context(data):
    ctx = build_context(data)
    scoring = calculate_scoring(data)

    for i, (indicator, value, score) in enumerate(scoring['score_rows'], start=1):
        ctx[f'score_{i}_indicator'] = indicator
        ctx[f'score_{i}_value'] = value
        ctx[f'score_{i}_score'] = str(score)

    ctx['total_score'] = str(scoring['total_score'])
    ctx['net_income_calc'] = scoring['net_income_calc']
    ctx['solvency'] = scoring['solvency']
    ctx['max_loan_amount'] = scoring['max_loan_amount']
    ctx['conclusion_text'] = (
        f'На основании анализа предоставленных данных считаю возможным выдачу кредита '
        f'{ctx["full_name"]} в размере {ctx["loan_amount_fmt"]} для {ctx["loan_purpose"]} '
        f'на {ctx["loan_term"]} месяцев под {ctx["interest_rate"]}% годовых.'
    )
    return ctx


def generate_documents(data, templates_dir, output_dir):
    ensure_templates(templates_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ctx = _enrich_context(data)
    generated = []

    for filename in TEMPLATE_FILES:
        template_path = Path(templates_dir) / filename
        out_path = output_dir / filename
        render_docx(template_path, ctx, out_path)
        generated.append(out_path)

    return generated


def create_zip_archive(file_paths):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in file_paths:
            zf.write(path, path.name)
    buffer.seek(0)
    return buffer
