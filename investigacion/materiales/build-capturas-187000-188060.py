#!/usr/bin/env python3
"""Genera un escenario de captura por material para 187000 y 188060.

Un escenario por combinación evita que el presupuesto de eventos del proveedor
se agote tras varias selecciones. Cada archivo captura la red y conserva la
respuesta `project/knife`; el colector la separa por paso.

No incluye materiales personalizados: sus intervalos requieren un muestreo
aparte y no se habilitan con una sola captura.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "capturas-escenarios"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

MODELS = {
    "187000": {
        "url": "https://www.pacdora.com/es/dielines-detail/custom-pillow-box-dieline-187000",
        "cases": [
            {"materialId": 101, "group": "Cartulina blanca", "label": "Cartón blanco 250g", "thickness": 0.35},
            {"materialId": 102, "group": "Cartulina blanca", "label": "Cartón blanco 300g", "thickness": 0.42},
            {"materialId": 109, "group": "Cartulina kraft", "label": "Cartón kraft 250g", "thickness": 0.33},
            {"materialId": 110, "group": "Cartulina kraft", "label": "Cartón kraft 350g", "thickness": 0.46},
            {"materialId": 47, "group": "Papel arte", "label": "Papel estucado 200g", "thickness": 0.2},
            {"materialId": 42, "group": "Papel arte", "label": "Papel estucado 350g", "thickness": 0.32},
        ],
    },
    "188060": {
        "url": "https://www.pacdora.com/es/dielines-detail/custom-dimensions-polygonal-boxes-hexagonal-dieline-188060",
        "cases": [
            {"materialId": 100, "group": "Cartulina blanca", "label": "Cartón blanco 210g", "thickness": 0.27},
            {"materialId": 101, "group": "Cartulina blanca", "label": "Cartón blanco 250g", "thickness": 0.35},
            {"materialId": 102, "group": "Cartulina blanca", "label": "Cartón blanco 300g", "thickness": 0.42},
            {"materialId": 104, "group": "Cartulina blanca", "label": "Cartón blanco 400g", "thickness": 0.55},
            {"materialId": 108, "group": "Cartulina kraft", "label": "Cartón kraft 190g", "thickness": 0.26},
            {"materialId": 109, "group": "Cartulina kraft", "label": "Cartón kraft 250g", "thickness": 0.33},
            {"materialId": 110, "group": "Cartulina kraft", "label": "Cartón kraft 350g", "thickness": 0.46},
            {"materialId": 47, "group": "Papel arte", "label": "Papel estucado 200g", "thickness": 0.2},
            {"materialId": 42, "group": "Papel arte", "label": "Papel estucado 350g", "thickness": 0.32},
            {"materialId": 10, "group": "Cartón corrugado", "label": "Onda N", "thickness": 0.8, "variable": True},
            {"materialId": 10, "group": "Cartón corrugado", "label": "Onda N", "thickness": 1.0, "variable": True},
            {"materialId": 6, "group": "Cartón corrugado", "label": "Onda F", "thickness": 1.0, "variable": True},
            {"materialId": 6, "group": "Cartón corrugado", "label": "Onda F", "thickness": 1.2, "variable": True},
            {"materialId": 5, "group": "Cartón corrugado", "label": "Onda E", "thickness": 1.1, "variable": True},
            {"materialId": 5, "group": "Cartón corrugado", "label": "Onda E", "thickness": 1.5, "variable": True},
            {"materialId": 5, "group": "Cartón corrugado", "label": "Onda E", "thickness": 2.0, "variable": True},
        ],
    },
}


def build_case(code, url, case):
    key = f"{code}-{case['materialId']}-{str(case['thickness']).replace('.', '_')}"
    actions = [
        {"action": "wait_for_timeout", "duration_ms": 3000, "step_id": "loaded"},
        {"action": "click", "locator": {"kind": "css", "selector": '[gtm="ga-dieline_dieline_basic_mm"]'}, "step_id": "mm", "timeout_ms": 8000},
        {"action": "click", "locator": {"kind": "css", "selector": ".material-select"}, "step_id": f"open-{key}", "timeout_ms": 8000},
        {"action": "click", "locator": {"kind": "css", "selector": f'.tree-select-item-header:text-is("{case["group"]}")'}, "button": "right", "step_id": f"group-{key}", "timeout_ms": 8000},
        {"action": "click", "locator": {"kind": "css", "selector": f'.tree-item:not(.disabled) .material-tree-item:has-text("{case["label"]}")'}, "step_id": f"pick-{key}", "timeout_ms": 8000},
        {"action": "wait_for_timeout", "duration_ms": 2500, "step_id": f"picked-{key}"},
    ]
    if case.get("variable"):
        actions += [
            {"action": "fill", "locator": {"kind": "css", "selector": ".thickness-control input"}, "value": {"source": "literal", "value": str(case["thickness"])}, "step_id": f"thick-{key}", "timeout_ms": 8000},
            {"action": "press", "locator": {"kind": "css", "selector": ".thickness-control input"}, "key": "Enter", "step_id": f"thick-{key}-apply", "timeout_ms": 8000},
            {"action": "wait_for_timeout", "duration_ms": 2000, "step_id": f"thick-{key}-ready"},
        ]
    actions.append({"action": "wait_for_timeout", "duration_ms": 5000, "step_id": f"settle-{key}"})
    scenario = {
        "browser": {"mode": "launch", "executable_path": CHROME, "headless": True},
        "start_url": {"url": url},
        "actions": actions,
        "capture": {
            "after_each_step": ["url"],
            "at_end": ["url"],
            "events": ["network"],
            "network": {"request_body": True, "response_body": True, "header_values": False},
        },
        "environment": {
            "locale": "es-CL",
            "timezone": "America/Santiago",
            "service_workers": "block",
            "viewport": {"width": 1280, "height": 900, "device_scale_factor": 1},
        },
    }
    path = OUT / f"{key}-scenario.json"
    path.write_text(json.dumps(scenario, ensure_ascii=False, indent=2) + "\n")
    return {
        "id": key,
        "model": code,
        "materialId": case["materialId"],
        "thickness": case["thickness"],
        "variableThickness": bool(case.get("variable")),
        "scenario": str(path.relative_to(ROOT)),
    }


def main():
    OUT.mkdir(exist_ok=True)
    index = []
    for code, spec in MODELS.items():
        for case in spec["cases"]:
            index.append(build_case(code, spec["url"], case))
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    print(len(index), "escenarios;", len(list(OUT.glob("*-scenario.json"))), "archivos")


if __name__ == "__main__":
    main()
