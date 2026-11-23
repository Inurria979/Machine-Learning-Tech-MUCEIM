"""Write analysis/notebook_dump.md: a readable, small view of the notebook for the agents.

For every cell: index, id, type, source, and TEXT outputs (stream, text/plain, errors), truncated to
150 lines per cell. Images are exported to figures/cell{idx:02d}_{n}.png and replaced by a placeholder line.
The figures/ folder is emptied first, so no obsolete figure survives. The Section 7 results table
(cell id 'frontier') is never truncated.
Usage: uv run python tools/dump_notebook.py
"""
import base64
import re
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / 'Lean_Network_Challenge.ipynb'
DUMP = ROOT / 'analysis' / 'notebook_dump.md'
FIGURES = ROOT / 'figures'
MAX_LINES = 150
NO_TRUNCATE = {'frontier'}  # cell ids whose output is dumped in full (the complete results table)
ANSI = re.compile(r"\[[0-9;]*m")  # strip terminal colour codes from outputs

DUMP.parent.mkdir(exist_ok=True)  # analysis/ was archived (D15); recreate it for the dump only
FIGURES.mkdir(exist_ok=True)
for old in FIGURES.glob('*.png'):  # remove figures of previous executions (cell indices may have changed)
    old.unlink()
nb = nbformat.read(NOTEBOOK, as_version=4)
out = []

for idx, cell in enumerate(nb.cells):
    cell_id = cell.metadata.get('id', '-')
    out.append(f'## [{idx:02d}] id={cell_id} type={cell.cell_type}')
    out.append('```' + ('python' if cell.cell_type == 'code' else 'markdown'))
    out.append(cell.source)
    out.append('```')
    if cell.cell_type != 'code':
        out.append('')
        continue

    lines, n_img = [], 0
    for o in cell.get('outputs', []):
        if o.output_type == 'stream':
            lines.extend(ANSI.sub('', o.text).rstrip('\n').split('\n'))
        elif o.output_type in ('display_data', 'execute_result'):
            data = o.get('data', {})
            if 'image/png' in data:
                path = FIGURES / f'cell{idx:02d}_{n_img}.png'
                path.write_bytes(base64.b64decode(data['image/png']))
                lines.append(f'[IMAGE: figures/{path.name}]')
                n_img += 1
            elif 'text/plain' in data:
                lines.extend(data['text/plain'].rstrip('\n').split('\n'))
        elif o.output_type == 'error':
            lines.append(f"ERROR {o.ename}: {o.evalue}")
    lines = [ANSI.sub('', l) for l in lines]
    if lines:
        total = len(lines)
        if total > MAX_LINES and cell_id not in NO_TRUNCATE:
            lines = lines[:MAX_LINES] + [f'... [truncated, {total - MAX_LINES} more lines]']
        out.append('Output:')
        out.append('```text')
        out.extend(lines)
        out.append('```')
    out.append('')

DUMP.write_text('\n'.join(out), encoding='utf-8')
print(f'Wrote {DUMP.relative_to(ROOT)} ({len(out)} lines) and figures/ images.')
