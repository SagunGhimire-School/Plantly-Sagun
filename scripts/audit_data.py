"""Read-only structural inventory; never approves science or imports source content."""
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def audit():
    inventory = json.loads((ROOT / "docs/curated_inventory.json").read_text())
    report = {"files": [], "scientific_approval": False}
    for relative, expected in inventory.items():
        path = ROOT / "data/curated" / relative
        if not path.is_file():
            report["files"].append({"path": relative, "missing": True})
            continue
        raw = path.read_bytes()
        data = yaml.safe_load(raw)
        rows = data if isinstance(data, list) else [data]
        ids = [row["id"] for row in rows if isinstance(row, dict) and "id" in row]
        report["files"].append({
            "path": relative, "sha256": hashlib.sha256(raw).hexdigest(),
            "exact_match": hashlib.sha256(raw).hexdigest() == expected["sha256"],
            "lf_match": hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest() == expected["sha256"],
            "records": len(rows), "ids": ids, "duplicate_ids": len(ids) != len(set(ids)),
            "fields": sorted({key for row in rows if isinstance(row, dict) for key in row}),
        })
    sources = yaml.safe_load((ROOT / "data/curated/rule_reviews/sources.yaml").read_text(encoding="utf-8"))
    report["sources"] = [{"id": s["id"], "url": s.get("url"), "legacy_verified": s.get("verified"), "license": s.get("license", "unknown")} for s in sources]
    return report


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
