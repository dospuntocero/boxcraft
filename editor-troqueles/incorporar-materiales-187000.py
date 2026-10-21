#!/usr/bin/env python3
"""Alta reproducible de los materiales verificados de 187000.

Los perfiles 100/0,27 y 108/0,26 se compararon con el corte base y son
idénticos; reutilizan la capa del modelo y quedan limitados a las medidas
comprobadas. No se habilitan materiales sin captura.
"""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
ASSETS = DIST / "assets"
CAPTURES = ROOT.parent / "investigacion/materiales/capturas-187000-188060"

MODEL_ID = "187000"
PROFILES = [
    {
        "materialId": 100,
        "thickness": 0.27,
        "capture": "187000-210g.html",
        "evidenceId": "ev_e47c1be1a068592c16db62f1f7eafa053c00fdfe935c2bb5fae670c16e9ea5a3",
    },
    {
        "materialId": 108,
        "thickness": 0.26,
        "capture": "187000-190g.html",
        "evidenceId": "ev_9f9f9c5433ef27591d4e864e7930435bd9757cb6124dfb6e3cc52c45251d99bb",
    },
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    models_path = ASSETS / "modelos.json"
    caps_path = ASSETS / "capacidades-materiales.json"
    models = json.loads(models_path.read_text())
    caps = json.loads(caps_path.read_text())
    model = next(m for m in models if m["id"] == MODEL_ID)
    cap = caps[MODEL_ID]
    dims = model.get("initialDims") or model["dims"]
    bounds = {axis: [value, value] for axis, value in dims.items()}

    profiles = []
    for item in PROFILES:
        capture = CAPTURES / item["capture"]
        if not capture.exists():
            raise SystemExit(f"Falta la captura {capture}")
        layer = copy.deepcopy(model["layer"])
        layer["science"] = {"id": item["materialId"], "name": f"material-{item['materialId']}"}
        layer["thickness"] = item["thickness"]
        profiles.append(
            {
                "materialIds": [item["materialId"]],
                "thickness": item["thickness"],
                "layer": layer,
                "offsets": {
                    "inner": {axis: 0 for axis in dims},
                    "outer": {axis: 0 for axis in dims},
                },
                "bounds": copy.deepcopy(bounds),
                "geometryStatus": "verified",
                "evidence": {
                    "configuration": dims,
                    "path": str(capture.relative_to(ROOT.parent)),
                    "sha256": sha256(capture),
                    "evidence_id": item["evidenceId"],
                    "comparison": "Corte idéntico al base; diferencia máxima 0,000 mm.",
                },
            }
        )

    # Idempotente: reemplaza solo las combinaciones incluidas en este script.
    kept = [
        p
        for p in cap.get("physicalProfiles", [])
        if not any(
            item["materialId"] in p.get("materialIds", [])
            and abs(p.get("thickness", -1) - item["thickness"]) < 1e-9
            for item in PROFILES
        )
    ]
    cap["physicalProfiles"] = kept + profiles
    # Rango observado en el menú de Pacdora para este modelo (0,20–0,50 mm).
    cap["observedThicknessLimits"] = [0.2, 0.5]
    cap["blockedReason"] = (
        "Materiales verificados: 350 g (original), 210 g (0,27 mm) y 190 g (0,26 mm). "
        "Faltan capturas para el resto del menú y para los espesores personalizados."
    )
    cap["source"] = (
        "motor pillow187000 + geometria/modelos/187000/muestras.json + "
        "investigacion/materiales/capturas-187000-188060/"
    )
    caps_path.write_text(json.dumps(caps, ensure_ascii=False, indent=2) + "\n")

    print(
        "187000:",
        len(cap["physicalProfiles"]),
        "perfiles;",
        "materiales compatibles:",
        sorted(
            {
                mid
                for p in cap["physicalProfiles"]
                for mid in p["materialIds"]
            }
            | {cap["originalMaterialId"]}
        ),
    )


if __name__ == "__main__":
    main()
