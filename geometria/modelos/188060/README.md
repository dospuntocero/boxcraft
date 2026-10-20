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

El modelo queda **fijo** en 100,6 × 40,6 × 181,6 mm y 0,5 mm. No se habilitó un motor paramétrico: no se probaron variaciones de L/W/H ni la topología del cierre hexagonal.

## Archivos

- `troquel-generado.svg`: plano vectorial a escala real.
- `troquel-generado.json`: geometría, extensión, conteos y procedencia.
- `vista-previa.png`: rasterización local del SVG (generada, no es una imagen oficial).
- `icono-3d.png`: recorte del visor 3D de Pacdora, usado como miniatura del catálogo; no es una descarga oficial.
- `base/knife-00.json`: respuesta original conservada.
- `base/geometria.json`: capa normalizada usada por el generador.
- `generar.py`: reproduce SVG/JSON sin red.
- `integrar.py`: alta en el catálogo, miniatura y capacidad de material.
- `validacion.json`: comprobaciones y hashes.

Desde `/Users/fran/Herd/pacdora`:

```sh
python3 geometria/modelos/188060/generar.py
/Users/fran/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3 geometria/modelos/188060/integrar.py
```

## Verificación y límites

- JSON y XML válidos; extensión positiva.
- 19 caras, 26 pliegues y 28 cortes; la geometría base se reproduce sin cambios.
- Se comprobó el alta en el catálogo local y la miniatura.
- No se validaron mínimos, otros materiales/espesores, armado físico, tolerancias ni exportación AI/DXF/PDF.
- La miniatura se generó desde la geometría local; no se presenta como imagen oficial de Pacdora.

## Evidencia

- Página y medidas iniciales: `ev_a75c36365ad2f0f766128a5055d1614f001124e94e80b155d14724abf291b669`.
- Respuesta de geometría base: `ev_0c2b9e45f786350aba1b5f6dc8e284902db9d8c40694ea89a7f9010bc4f8ebbc`.
