# Capturas de geometría · 187000 y 188060

Escenarios preparados el 2026-10-20 para completar los materiales que aún no tienen geometría capturada en el editor local.

## Archivos

| Archivo | Contenido |
|---|---|
| `build-capturas-187000-188060.py` | Genera un escenario por combinación |
| `capturas-escenarios/index.json` | Índice de los 22 escenarios: modelo, material, espesor y archivo |
| `capturas-escenarios/*-scenario.json` | Un escenario por material y espesor |
| `collect-capturas-materiales.py` | Separa las respuestas `project/knife` y las atribuye a cada paso |

Los materiales personalizados quedan fuera: sus intervalos continuos necesitan un muestreo propio y no se habilitan con una sola captura.

## Por qué un escenario por material

La carga completa de la página consume cerca del presupuesto de eventos del proveedor. Un escenario con varias selecciones puede truncar la respuesta `project/knife` de las últimas. Separar cada combinación evita esa pérdida y permite repetir solo la que falle. Los escenarios usan `after_each_step: ["url"]` para vaciar el registro entre pasos y una espera de 5 s para que la respuesta de geometría se complete.

## Ejecutar

1. Leer `capturas-escenarios/index.json`.
2. Para cada entrada, cargar su `scenario` y pasar `browser`, `start_url`, `actions`, `capture` y `environment` a `capture_browser_scenario`.
3. Guardar el resultado como `capturas-escenarios/<id>-result.json`.
4. Comprobar que la respuesta tenga `completeness.dropped_events.total == 0` y que exista al menos un `project/knife`.
5. Separar las geometrías:

```sh
python3 investigacion/materiales/collect-capturas-materiales.py \
  investigacion/materiales/capturas-escenarios/*-result.json
```

El colector escribe `samples/capturas-materiales/<modelo>/<material>-<espesor>/knife-<secuencia>.json` y el resumen `capturas-materiales.json`. Marca `mismatch` cuando `layer.traditional.science_id` o `thickness` no coinciden con el paso.

## Criterios de aceptación

- Cada paso `pick-<material>-<espesor>` debe producir al menos una respuesta `project/knife`.
- La selección efectiva se comprueba en `layer.traditional.science_id` y `layer.traditional.thickness`, no solo en el control visible.
- Para 187000 se compara el corte con la capa base: si es idéntico, el perfil puede reutilizarla; si difiere, se guarda la capa propia.
- Para 188060 se guarda la capa propia y sus compensaciones `size`/`outSize`; no se reutiliza la base.
- Los extremos de Onda N (0,8/1,0), Onda F (1,0/1,2) y Onda E (1,1/2,0) se capturan antes de habilitar el control continuo.

## Limitaciones

- La captura usa la interfaz pública; no se usó cuenta ni se descargaron archivos.
- La captura de red conserva todas las respuestas, no solo `project/knife`; el colector filtra por URL.
- El presupuesto de eventos del proveedor puede truncar una captura incluso con un solo material; en ese caso se repite el escenario y se conserva el resultado anterior como parcial.
- Una captura correcta no acredita armado físico ni equivalencia completa con el servicio.
