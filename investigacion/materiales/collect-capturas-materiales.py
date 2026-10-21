#!/usr/bin/env python3
"""Separa las respuestas project/knife de los resultados de captura de materiales.

Uso:
  python3 collect-capturas-materiales.py 187000-materiales-result.json 188060-materiales-result.json

Escribe `samples/capturas-materiales/<modelo>/<material>-<espesor>/knife-<seq>.json`
y un resumen `capturas-materiales.json` con la atribución por paso.
"""
import base64
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "samples" / "capturas-materiales"


def scenario_of(record):
    """Acepta un resultado normalized_result o un registro de evidencia completo."""
    result = record.get("normalized_result")
    if result:
        return result
    details = record.get("details", {})
    partial = details.get("partial_observation", {}).get("capture", {})
    return partial.get("error", {}).get("details", {}).get("partial_observation", {}).get("capture", partial)


def expected_from_step(step_id):
    """pick-100-0_27 -> (100, 0.27); thick-5-1_1 -> (5, 1.1)."""
    if not step_id or not (step_id.startswith("pick-") or step_id.startswith("thick-")):
        return None
    parts = step_id.split("-")
    if len(parts) < 3:
        return None
    try:
        return int(parts[1]), float(parts[2].replace("_", "."))
    except ValueError:
        return None


def latest_step(step_ids, index):
    """Último paso de selección/espesor en o antes del evento de red."""
    candidates = [
        (i, step_id)
        for i, step_id in step_ids.items()
        if i <= index and (step_id.startswith("pick-") or step_id.startswith("thick-"))
    ]
    return max(candidates)[1] if candidates else ""


def main(paths):
    records = []
    for path in paths:
        raw = path.read_text()
        data = json.loads(raw)
        recs = data.get("records", [data])
        for rec in recs:
            result = scenario_of(rec)
            if not result.get("steps"):
                continue
            evidence = rec.get("evidence_id") or "sha256-" + hashlib.sha256(path.read_bytes()).hexdigest()
            steps = result["steps"]
            step_ids = {s["step_index"]: s["step_id"] for s in steps}
            events = result.get("events", {}).get("items", [])
            requests = {e["transaction_id"]: e for e in events if e.get("kind") == "request"}
            samples = []
            for event in events:
                if event.get("kind") != "network-content" or event.get("phase") != "response":
                    continue
                body = event.get("body", {})
                if not body.get("content"):
                    continue
                request = requests.get(event["transaction_id"], {})
                url = request.get("url", {}).get("url", "")
                if "/project/knife" not in url:
                    continue
                try:
                    payload = json.loads(base64.b64decode(body["content"]))
                except Exception:
                    continue
                knife = payload.get("data")
                if not isinstance(knife, dict):
                    continue
                layer = (knife.get("layer") or {}).get("traditional") or {}
                science = knife.get("science") or {}
                model = str(knife.get("cate_no", ""))
                material = layer.get("science_id", science.get("id"))
                thickness = layer.get("thickness", science.get("thickness"))
                step_index = event.get("step_index")
                step_id = latest_step(step_ids, step_index)
                expected = expected_from_step(step_id)
                folder = OUT / model / f"{material}-{thickness}"
                folder.mkdir(parents=True, exist_ok=True)
                dest = folder / f"knife-{event['sequence']}.json"
                dest.write_text(json.dumps(payload, ensure_ascii=False))
                sample = {
                    "model": model,
                    "materialId": material,
                    "thickness": thickness,
                    "expected": {"materialId": expected[0], "thickness": expected[1]} if expected else None,
                    "mismatch": bool(expected and (expected[0] != material or abs(expected[1] - thickness) > 1e-9)),
                    "knifeSize": knife.get("knifeSize"),
                    "size": knife.get("size"),
                    "outSize": knife.get("outSize"),
                    "step": step_index,
                    "stepId": step_id,
                    "sequence": event["sequence"],
                    "file": str(dest.relative_to(ROOT)),
                    "evidenceId": evidence,
                }
                samples.append(sample)
            if samples:
                records.append({"file": path.name, "evidenceId": evidence, "samples": samples, "stepIds": step_ids})

    (ROOT / "capturas-materiales.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    total = sum(len(r["samples"]) for r in records)
    mismatches = sum(1 for r in records for s in r["samples"] if s["mismatch"])
    print(f"{total} respuestas de geometría; {mismatches} discrepancias de material/espesor")
    for record in records:
        print(record["file"], len(record["samples"]), "knives")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main([Path(p) for p in sys.argv[1:]])
