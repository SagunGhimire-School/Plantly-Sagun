"""Local read-only dependency and curated-file presence check. Python stdlib only."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def check(name: str, command: list[str]) -> None:
    exe = shutil.which(command[0])
    if not exe:
        print(f"[MISSING] {name}: {command[0]} not found on PATH")
        return
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=9, check=False)
        first = ((result.stdout or result.stderr) or '').strip().splitlines()
        detail = first[0] if first else f"exit code {result.returncode}"
        label = 'OK' if result.returncode == 0 else 'NOT READY'
        print(f"[{label}] {name}: {detail[:160]}")
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"[NOT READY] {name}: {error}")


def main() -> None:
    print('Plantly: read-only setup preflight (does not install or modify anything)')
    print(f"[{'OK' if sys.version_info >= (3, 12) else 'UPDATE'}] Python: {sys.version.split()[0]} (requires 3.12+)")
    check('Node.js', ['node', '--version'])
    check('npm', ['npm.cmd' if sys.platform == 'win32' and shutil.which('npm.cmd') else 'npm', '--version'])
    check('Git', ['git', '--version'])
    check('Docker', ['docker', '--version'])
    check('Docker Compose', ['docker', 'compose', 'version'])
    check('Docker engine', ['docker', 'info', '--format', '{{.ServerVersion}}'])

    inventory = json.loads((ROOT/'docs/curated_inventory.json').read_text(encoding='utf-8'))
    missing, matched, line_endings, mismatched = [], [], [], []
    for relative, record in sorted(inventory.items()):
        target = ROOT/'data/curated'/relative
        if not target.is_file():
            missing.append(relative)
        else:
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual == record['sha256']:
                matched.append(relative)
            elif hashlib.sha256(target.read_bytes().replace(b'\r\n', b'\n')).hexdigest() == record['sha256']:
                line_endings.append(relative)
            else:
                mismatched.append(relative)
    print(f"\nCurated original files: {len(matched)}/{len(inventory)} hashes match the supplied inventory")
    print(f"Windows line-ending differences only: {len(line_endings)} (original bytes preserved)")
    if missing:
        print('Missing (okay for M-001, required later for real ingestion):')
        for item in missing:
            print('  - data/curated/' + item)
    if mismatched:
        print('WARNING: content hashes differ; inspect originals (do not rewrite just to match):')
        for item in mismatched:
            print('  - data/curated/' + item)
    for rel in ['frontend/public/brand/planty_logo.svg', 'frontend/public/brand/premium_spherical_plant_emblem.png', 'frontend/public/images/golden_harvest_tractor_at_sunset.png']:
        print(f"[{'OK' if (ROOT/rel).is_file() else 'OPTIONAL MISSING'}] Artwork: {rel}")
    print('\nThe first Codex milestone does not require curated data, paid APIs or artwork.')


if __name__ == '__main__':
    main()
