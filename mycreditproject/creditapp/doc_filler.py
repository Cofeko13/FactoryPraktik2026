import re
import shutil
import zipfile
from pathlib import Path

PLACEHOLDER_RE = re.compile(r'\{\{\s*(\w+)\s*\}\}')

# можно еще _escape_xml
def _escape_xml(text):
    if text is None:
        return ''
    text = str(text)
    return (
        text.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
    )


def render_docx(template_path, context, output_path):
    context = {k: _escape_xml(v) for k, v in context.items()}
    template_path = Path(template_path)
    output_path = Path(output_path)

    with zipfile.ZipFile(template_path, 'r') as zin:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename.startswith('word/') and item.filename.endswith('.xml'):
                    text = data.decode('utf-8')

                    def replacer(match):
                        key = match.group(1)
                        return context.get(key, '')

                    text = PLACEHOLDER_RE.sub(replacer, text)
                    data = text.encode('utf-8')
                zout.writestr(item, data)
