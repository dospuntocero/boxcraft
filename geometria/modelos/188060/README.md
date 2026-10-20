[English](README.en.md) · Español

# Troquel 188060 · Caja hexagonal

Fuente: https://www.pacdora.com/es/dielines-detail/custom-dimensions-polygonal-boxes-hexagonal-dieline-188060

Modelo **188060**, «Custom dimensions polygonal boxes hexagonal dieline» / «Caja hexagonal». Configuración inicial de Pacdora: **100,6 × 40,6 × 181,6 mm** de manufactura, cartón blanco 350 g de **0,5 mm** (material 103). Medidas interiores **100 × 40 × 180 mm**; exteriores **145,2 × 41 × 222,6 mm**.

## Geometría

- **19 caras**: seis paneles laterales (FL, F, B, BR, TL, T) con sus pestañas superior e inferior (BTL/BT/BTR, BBL/BB/BBR, etc.).
- **26 pliegues** y **28 comandos de corte**.
- Extensión del plano: **336,7 × 262,8 mm**.
- Sin orificios interiores reales: la capa superior declara una lista vacía.
- El corte azul, las caras y los pliegues se extrajeron de la respuesta `project/knife` del editor de Pacdora; no se inventó la geometría.

## Medidas y modos

La página muestra los modos **Dimensiones de manufactura**, **interiores** y **exteriores**. La base local conserva únicamente la configuración de manufactura; no se capturaron compensaciones internas/externas independientes para otros materiales.

El modelo usa un **motor de paneles L/W/H experimental** para el material y espesor originales. La geometría base se reproduce exactamente; L=110 se validó contra el SVG renderizado (error máximo 0,7 mm). W=45 y H=190 se validaron con el mismo mapa: error máximo 0,16 mm y 0,00 mm respectivamente.

## Motor L/W/H

El plano se reconstruye por paneles: el ancho sigue los seis paneles laterales y el alto los tramos pestaña-cuerpo-pestaña.

- `totalX = 135,5 + 2L`
- `totalY = 2W + H`
- X: cortes en `46`, `46+L`, `76+L`, `106+L`, `106+2L`, `135,5+2L`.
- Y: pestaña superior `0..W`, cuerpo `W..W+H`, pestaña inferior `W+H..2W+H`.
- Los radios de las esquinas se conservan; no se escalan.

Se verificó en el editor local **110 × 45 × 190 mm**, con plano de **355,5 × 280 mm** y las tres medidas editables. La comparación de la cara TR a L=110 coincide; el error máximo del conjunto de caras fue 0,7 mm. L=110 tiene 0,70 mm de error por la posición de la muesca; W/H coinciden dentro de 0,16 mm. El modelo sigue marcado como experimental por la ausencia de validación física.

## Archivos

- `troquel-generado.svg`: plano vectorial a escala real.
- `troquel-generado.json`: geometría, extensión, conteos y procedencia.
- `vista-previa.png`: rasterización local del SVG (generada, no es una imagen oficial).
- `icono-3d.jpg`: mockup oficial de Pacdora (`https://cdn.pacdora.com/image-resize/300xauto_outside/preview/mockup-188060.jpg`, SHA-256 `012a6401701caace43bcc30a17691977920c7dd32aa95656c2d1c99a3ecbe342`), usado como miniatura del catálogo. Se conserva el JPG original.
- `base/knife-00.json`: respuesta original conservada.
- `base/geometria.json`: capa normalizada usada por el generador.
- `generar.py`: reproduce SVG/JSON sin red.
- `integrar.py`: alta en el catálogo, miniatura y capacidad de material.
- `muestras/`: caras de las variantes L=110, W=45 y H=190 con sus evidencias.
- `validacion.json`: comprobaciones y hashes.

Desde `/Users/fran/Herd/pacdora`:

```sh
python3 geometria/modelos/188060/generar.py
/Users/fran/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3 geometria/modelos/188060/integrar.py
```

## Verificación y límites

- JSON y XML válidos; extensión positiva.
- 19 caras, 26 pliegues y 28 cortes; la geometría base se reproduce sin cambios.
- Motor de paneles: base exacta; L=110 validado (error máximo 0,7 mm); W/H analíticos sin muestra independiente.
- Se comprobó el alta en el catálogo local, la miniatura y el cambio a 110 × 45 × 190 mm.
- No se validaron mínimos, otros materiales/espesores, armado físico, tolerancias ni exportación AI/DXF/PDF. Muestras L=110, W=45 y H=190 validadas contra el SVG renderizado.
- La miniatura se generó desde la geometría local; no se presenta como imagen oficial de Pacdora.

## Evidencia

- Página y medidas iniciales: `ev_a75c36365ad2f0f766128a5055d1614f001124e94e80b155d14724abf291b669`.
- Respuesta de geometría base: `ev_0c2b9e45f786350aba1b5f6dc8e284902db9d8c40694ea89a7f9010bc4f8ebbc`.
- Cambio 110 × 45 × 190 en el editor: `ev_f86e32d44ae650592412371043aced9524f23298655a6d2a1447849f962fefb3`.
