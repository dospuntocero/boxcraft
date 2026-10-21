# Parametrización · capturas y ajuste

Herramientas para capturar geometría de Pacdora y ajustar reglas locales sin consultar el servicio al abrir o exportar.

## Estado

- **Verificados digitalmente:** 187000, 366010, 10002003 y 10001006. Sus informes están en `geometria/modelos/<código>/validacion-parametrica.json`.
- **Experimentales:** 112047, 12109002, 112310, 180370, 180320, 15030101, 102010 y 188060. Conservan sus motores actuales y sus advertencias.
- **Capturas preparadas para la siguiente pasada:** 180320 (150, rejillas densas L/W) y 112047 (496 celdas L×W a 1 mm + barridos 0,1 mm). En 180320 falta el régimen no lineal; en 112047 los parámetros están resueltos salvo la función 1D de W, y las tablas de 1/2 mm se probaron y no alcanzan 0,1 mm.

El estado del catálogo se aplica con `editor-troqueles/aplicar-estados.py`; no se escribe a mano en `modelos.json`.

## Capturar

`capturar-playwright.cjs` abre una sesión de Chrome, fija el material original y recorre una matriz L/W/H. Guarda cada respuesta `/project/knife` y un `manifest.json`.

```sh
node investigacion/parametrico/capturar-playwright.cjs \
  --plan /tmp/plan-112310.json \
  --out /tmp/capturas-112310
```

El plan tiene esta forma:

```json
{"url":"https://www.pacdora.com/es/dielines-detail/...","materialId":5,"thickness":1.5,
 "configs":[{"L":302,"W":152,"H":182},{"L":310,"W":156,"H":186}],
 "loadMs":4000,"stepMs":700,"waitMs":1600}
```

La primera configuración debe diferir de la configuración inicial de la página; si no, no hay respuesta nueva. Para capturar la base, cámbiala primero y vuelve a ella.

## Ajustar

`ajustar-playwright.py` fusiona las muestras históricas (`parametricas/`) con directorios nuevos, deriva fórmulas para `openParams` y ajusta la geometría como combinación afín de L/W/H y esos parámetros. Reserva holdouts y solo escribe reglas si el error es exacto.

```sh
python3 investigacion/parametrico/ajustar-playwright.py 112310 /tmp/capturas-112310
```

Limitaciones actuales del ajustador:

- Las fórmulas candidatas cubren una o dos dimensiones con `round/floor/ceil/clamp`; no cubren todavía arcos, raíces ni funciones por tramos.
- 112310 y 112047 exponen parámetros internos, pero parte de la geometría no se explica solo con ellos y el error residual supera 1e-4 mm. No se marcan como verificados. 10002003 sí se cerró con reglas compiladas y 49 capturas.
- 12109002, 188060, 15030101, 102010 y los paneles requieren detección de topologías/arcos y capturas adicionales.

## Validar

`editor-troqueles/tests/parametric-verified.test.cjs` comprueba los modelos verificados. `editor-troqueles/comprobar-parametrizacion.cjs` conserva comprobaciones de mecánica, pero todavía tiene ramas históricas que no cubren todos los motores actuales.
