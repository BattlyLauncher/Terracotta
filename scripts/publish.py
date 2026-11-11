"""Publish a new version without replacing existing release assets."""
import json
import os
import pathlib
import re
import subprocess

version = os.environ['TERRACOTTA_VERSION']
repo = os.environ['GITHUB_REPOSITORY']
sha = os.environ['GITHUB_SHA']
if not re.fullmatch(r'\d+\.\d+\.\d+-battly\.\d+', version) or not re.fullmatch(r'[a-f0-9]{40}', sha):
    raise RuntimeError('Invalid release identity')

def gh(*args):
    return subprocess.check_output(['gh', *args], text=True, timeout=120)

pages = json.loads(gh('api', f'repos/{repo}/releases?per_page=100', '--paginate', '--slurp'))
existing = next((r for page in pages for r in page if r['tag_name'] == f'v{version}'), None)
if existing:
    if existing['draft']:
        raise RuntimeError('Inspect the existing draft before retrying')
    print('Version already published; existing assets unchanged.')
else:
    files = sorted(pathlib.Path('bundle').iterdir())
    manifest = json.loads(pathlib.Path('bundle/manifest-multiplatform.json').read_text())
    expected = {a['name'] for a in manifest['assets']} | {'LICENSE', 'battly.patch', 'SHA256SUMS', 'manifest-multiplatform.json'}
    if len(manifest['assets']) != 13 or {p.name for p in files} != expected or any(not p.is_file() for p in files):
        raise RuntimeError('Unexpected release contents')
    gh('release', 'create', f'v{version}', *(str(p) for p in files), '--repo', repo,
       '--target', sha, '--title', f'Terracotta {version} · Battly multiplatform',
       '--notes-file', 'release-notes.md', '--draft')
    gh('release', 'edit', f'v{version}', '--repo', repo, '--draft=false')
