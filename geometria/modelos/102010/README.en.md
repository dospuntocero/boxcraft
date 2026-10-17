[Español](README.md) · English

# Dieline 102010 · Snap-lock bottom closure

Source: https://www.pacdora.com/es/dielines-detail/custom-dimensions-tuck-end-boxes-auto-bottome-snap-lock-dieline-102010

At the user's request, the initial manufacturing dimensions are retained: **120.6 × 60.6 × 161.1 mm**, 350 g white paperboard, **0.5 mm** thick. The family returned by the server is PairBuckle. The blank measures 377.9 × 282.25 mm and contains 13 faces, 12 folds, and 80 cut commands.

## Files

- troquel-generado.svg: local blank with colored faces, red cuts, and dashed blue folds.
- troquel-generado.json: local geometry with dimensions and provenance.
- generar.py: reproduces the blank offline without external dependencies.
- reglas-altura.json and validacion-generador.json: empirical height rule and its check.
- muestras/: original responses and capture-stage manifest.

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/102010/generar.py
```

Replaces the output SVG and JSON. The default retains the initial dimensions exactly. Length and width remain fixed. Advanced controls are not exposed.

An experimental `--height` option is retained, between 161.1 and 190.5 mm. Its rule was inferred from two responses with L=139.7 and W=76.2, then checked on another pair, L=129.54 and W=68.58, changing H=190.5 to H=177.8: all 857 compared numeric fields matched within 0.000001 units. Check data were not used to fit the rule. Applying it to noninitial heights at L=120.6 and W=60.6 is an empirical transfer, not a second direct server check.

## Bottom structure change

A single linear fit was not applied to length and width. At L=139.7, W=60.6, and H=161.1, the server returned 92 cut commands and S1=1, versus 80 commands and S1=0 in the base. With W=76.2, it returned to 80 commands. This is a structural change, not coordinate scaling. Full samples remain available for future analysis if other dimensions are needed.

## Verification and limitations

Default output geometry matches the original layer in every included field. SVG XML, output dimensions, face/fold counts, and the independent height check were verified. Bleed and sizeArrowData annotations were excluded from both output and height comparison. Arcs use SVG A commands with the returned fields; their interpretation was not visually compared with the editor.

Colors are for inspection. A physical sample, actual folding, production tolerances, and AI/DXF/PDF export were not checked. Not validated for manufacturing.

## Evidence

- Initial inspection: ev_c6ea1b036de1ac294d9e3583195505c1ec266575314f7ee931adc64f29436088.
- Initial geometry after recovery: ev_d1a199a17596b35f91edc2663082fe51f7e8dee1d3e8ea30e3b1605d3502ea79.
- Samples and height check: ev_0a7239223cabad80da05402c2a2ce706c070f982ebc2bf7269b14408127c2ff2.

The first variation captures exhausted the 300 s MCP limit. A temporary REA browser left open was diagnosed and closed with authorization. The captures were then recovered. The final sample capture reported cleanup_incomplete; its partial observation was exported, with all recorded actions completed and all responses used present. Its lifecycle is not presented as complete. Geometry and compared fields come from retained responses, not attempts without results.
