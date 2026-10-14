"""Static publication checks; does not call APIs or load any model."""
import ast
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []
for path in root.rglob('*'):
    if not path.is_file() or '.git' in path.parts:
        continue
    relative = path.relative_to(root)
    if path.stat().st_size > 1_000_000:
        errors.append(f'{relative}: unexpected large file')
    text = path.read_text(encoding='utf-8-sig')
    if re.search(r'sk-' + r'[A-Za-z0-9_-]{20,}', text):
        errors.append(f'{relative}: possible credential (value suppressed)')
    if re.search(r'[A-Za-z]:' + r'\\(?:Users|Desktop)\\', text):
        errors.append(f'{relative}: private absolute path')
    if path.suffix == '.ipynb':
        nb = json.loads(text)
        for index, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'code':
                if cell.get('outputs') or cell.get('execution_count') is not None:
                    errors.append(f'{relative} cell {index}: saved execution state')
                code = ''.join(cell['source'])
                ast.parse(code)
                if re.search(r'os\.environ\[.*OPENAI_API_KEY.*\]\s*=', code):
                    errors.append(f'{relative} cell {index}: embedded key assignment')
if errors:
    raise SystemExit('\n'.join(errors))
print('PASS: notebook JSON, Python syntax, outputs, credential patterns, paths and file sizes.')
