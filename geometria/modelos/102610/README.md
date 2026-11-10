# Troquel 102610 · Caja con apertura trasera

Fuente pública: https://www.pacdora.com/es/dielines-detail/custom-dimensions-back-open-boxes-double-tray-dieline-102610

La URL compartida con `?id=72128964` exige iniciar sesión en Pacdora; se usó la página pública del modelo. Identidad verificada: `cate_no` **102610**, código **PairBackopenForward**, nombre original **后开正向插锁盒** (caja con apertura trasera).

## Medidas iniciales

| Modo | L | W | H |
|---|---|---|---|
| Interior (`size`) | 120 | 60 | 160 |
| Manufactura (`knifeSize`) | **120,6** | **60,6** | **161,6** |
| Exterior (`outSize`) | 121 | 61 | 162 |

Material: **cartón blanco 350 g de 0,5 mm** (science 103). Plano de **377,9 × 311,3 mm**, con **13 caras, 12 pliegues, 83 comandos de corte y 0 aberturas**. Longitud de pliegue calculada 1.331,3387 mm (declarada 1.331,34); longitud de corte declarada 1.644,36 mm.

## Archivos y uso

- `troquel-generado.svg` / `troquel-generado.json`: reconstrucción local.
- `vista-previa.png`: render revisado.
- `generar.py`: regenera SVG y JSON sin red.
- `validar.py`: comprueba la salida y escribe `validacion.json`.
- `base/knife-00.json`, `base/manifest.json`: respuesta inicial y procedencia.
- `parametrico/`: 76 capturas con manifiesto y SHA-256.
- `reglas-parametricas.json`, `validacion-parametrica.json`: motor compilado.
- `compilar-reglas.py`, `integrar.py`: recompilación y alta en el editor.
- `icono.jpg`, `icono.manifest.json`: miniatura oficial.

```sh
python3 geometria/modelos/102610/generar.py
python3 geometria/modelos/102610/validar.py
python3 geometria/modelos/102610/compilar-reglas.py
python3 geometria/modelos/102610/integrar.py
```

## Estructura

| Cara | Tamaño (mm) | Papel observado |
|---|---|---|
| HL | 16 × 160,6 | solapa de encolado |
| H | 120,6 × 161,6 | frontal |
| FL / FR | 60,6 × 161,6 / 60,1 × 161,6 | laterales |
| F | 120,6 × 161,6 | trasera |
| FT / FB | 120,6 × 60,6 | solapas superior e inferior |
| FT1 / FB1 | 119,6 × 15 | pestañas de cierre |
| FLT / FLB / FRT / FRB | 60,6 / 60,1 × 38 | pestañas laterales |

La topología (13/12/83/0) se mantuvo en las 76 capturas, entre 60 × 20 × 50 y 200 × 100 × 250 mm.

## Materiales

La respuesta fija `science` 103 con `can_set = 0` y espesor mínimo = máximo = 0,5 mm. No se capturaron otros materiales ni espesores. El selector de la página no se recorrió para este modelo.

## Límites

- Límites de interfaz: L 20–2000, W 10–2000, H 40–2000 mm.
- Rango habilitado: **L 60–200, W 20–100, H 50–250 mm**.
- H 40,6 no emitió respuesta en la captura; por eso el mínimo habilitado es H 50.

## Parámetros internos

En el rango habilitado, los parámetros se explican exactamente (76 capturas) por:

| Parámetro | Regla observada |
|---|---|
| `C` / `CR` | 13/7 para L < 100; 15/8 para L < 130; 20/10 para L < 180; 25/13 desde 180 |
| `E` / `S` | 6/4 para L < 65; 8/6 para L < 150; 11/9 desde 150 |
| `G` | 19 si `L+W ≥ 250,25`; 16 si `L+W ≥ 125,25`; 13 en el resto |
| `A` | `min(floor(L/2), floor((ceil(W) + C + 0,5)/2 + 0,5))` |
| `AR` | 1 si W ≤ 30; `floor((W + C)/8)` si W > 30 |
| `NX` / `NY` | 2 si W ≤ 30; 3 si W > 30 |
| `ATT` | 13 salvo W = 20, donde vale 0 |

## Motor verificado

La geometría es afín por tramos de anchura:

- `W = 20`: 10 muestras.
- `21 ≤ W ≤ 29`: 11 muestras.
- `W = 30`: 7 muestras.
- `W > 30`: 48 muestras.

**76 capturas dentro del rango**, error máximo **1,93 × 10⁻¹² mm**. El motor se integró como `compiled`; el modelo aparece como **Caja con apertura trasera (102610)**.

Se añadió soporte para comandos de trazado **Q** (curvas cuadráticas) en el visor y en el cálculo de sangrado, necesarios para las esquinas de este troquel.

## Verificación

- 803 campos numéricos idénticos a la respuesta base.
- SVG con 13 caras y 12 pliegues; 0 aberturas.
- Pliegue calculado 1.331,338675 mm frente a 1.331,34 declarado.
- Motor compilado exacto en las 76 capturas.
- Pruebas del editor: 101/101.

No se validó armado físico, tolerancias, otros materiales ni exportaciones AI/DXF/PDF. La equivalencia digital no acredita aptitud de fabricación.

## Evidencia

- Respuesta base: `base/knife-00.json`, SHA-256 `18ea2ef87c6754acc1d75be3a790e1601802017c6e74553fbca5bd727d0b36b9`.
- Capturas: `parametrico/manifest.json`, 76 archivos con SHA-256.
- Icono: `modeCate.image`, SHA-256 `b576cfdf9a4eb9798be69d3d61f2ac599a64a7d21218b0136071f726c82dca9a`.
- Capturas con Playwright el 2026-11-10; la URL con `?id=72128964` quedó bloqueada por inicio de sesión.
