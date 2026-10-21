# Parametrización de los ocho modelos que tenían medidas fijas

## Estado actual de la parametrización (20/10/2026)

Solo se marca **verificado** un modelo cuyo motor reproduce exactamente las capturas de referencia y cuyos holdouts independientes pasan. El estado se deriva de `geometria/modelos/<código>/validacion-parametrica.json`; no se escribe a mano.

| Modelo | Estado | Evidencia | Falta para cerrar |
|---|---|---|---|
| 187000 | **Verificado digital** | 7 capturas; corte 0,00007 mm; caras 0,00003 mm | Validación física; bordes adicionales de `rt`/`y0` |
| 366010 | **Verificado digital** | 58 capturas; 0,000 mm fuera de `/bleeds`; regímenes A/B | Validación física; ampliar rango |
| 112047 | Experimental | 138 capturas densas | `M` y `K3` exactos; no linealidad 1D de W con muescas de redondeo en 48,2–48,6 y 54,4–54,6; falta fórmula cerrada |
| 12109002 | Experimental | 3 holdouts hasta 1,57 mm | Detección de escalones y puntos de quiebre |
| 112310 | Experimental | 2 holdouts hasta 2,50 mm | Fórmulas de `H1,HT,K1,K3,SP,MR` |
| 10001006 | **Verificado digital** | 97 capturas; 0,000 mm; reglas compiladas en `A/AR/C/CR/E/NX/NY` | Validación física |
| 10002003 | **Verificado digital** | 49 capturas; 0,000 mm; reglas compiladas en `A/AR/C/CR/G/L1/NX/NY` | Validación física |
| 180370 | Experimental | 3 holdouts hasta 0,54 mm | Fórmulas de arcos y `D1/L1/L2/W1` |
| 180320 | Experimental | 150 capturas; la mayoría de parámetros con fórmulas exactas | La geometría no es afín en esos parámetros en el barrido denso de L; falta el régimen no lineal |
| 15030101 | Experimental | 3,88 mm; `enabled=false` | Topología pequeña y regla exacta grande |
| 102010 | Experimental | 1,82 mm; solo topología 80 cortes | Topología 92 cortes y regla exacta |
| 188060 | Experimental | L 0,70 mm | Muesca exacta y W/H independientes |

La infraestructura de captura y ajuste está en `investigacion/parametrico/`. Las capturas nuevas se guardan por modelo y no sobrescriben las históricas.

Los ocho modelos ya tienen generadores locales. La selección, los campos de medidas, la conversión mm/in, las capas y el SVG usan la misma geometría generada. El material y el espesor siguen fijos.

| Modelo | Ejes nuevos | Método | Alcance |
|---|---|---|---|
| 150010 · Mailer | L/W/H | Reglas por coordenada obtenidas de variaciones de dimensiones | Dos muestras adicionales coinciden en los 1.297 campos numéricos; rango observado 315–330 / 202–212 / 62–66 mm |
| 112047 · Techo y cordón | L/W/H | Reglas por parámetros + tabla 1D de W | Experimental; parámetros exactos, pero la no linealidad de W no tiene fórmula cerrada y las tablas de 1/2 mm no alcanzan 0,1 mm |
| 12109002 · Pastel | L/W/H | Reglas empíricas por coordenada | Experimental; diferencia máxima 1,574 |
| 112310 · Asa y fondo | L/W/H | Reglas empíricas por coordenada | Experimental; diferencia máxima 2,5 |
| 10001006 · Solapas | L/W/H | Reglas compiladas en parámetros internos | Verificado digital; 97 capturas y error 0,000 mm |
| 10002003 · Colgar | L/W/H | Reglas compiladas en parámetros internos | Verificado digital; 49 capturas y error 0,000 mm |
| 180370 · Papas fritas | L/W/H | Reglas empíricas por coordenada, conservando arcos | Experimental; diferencia máxima 0,536 |
| 180320 · Sándwich | L/W | Transformación por paneles y diagonales | Experimental; 150 capturas y fórmulas de la mayoría de parámetros, pero falta el régimen no lineal |

Las diferencias anteriores incluyen todos los campos numéricos del plano, no son una tolerancia física de fabricación. Los campos de coordenadas y longitudes están en mm. Los valores completos están en `validacion-parametrizacion.json`. No se presenta una comparación fallida como validación aprobada.

Los motores aún experimentales ofrecen adaptación de la geometría, pero no reproducen todos los ajustes automáticos y redondeos del servicio original. Se señalan en el catálogo y el panel de medidas. 187000, 366010, 10002003 y 10001006 ya están verificados digitalmente; el resto conserva rangos observados y advertencias. Se necesita una muestra física para confirmar el armado.

Los tres modelos que ya eran editables mantienen sus reglas: 200010 y 10001029 admiten L/W/H; 102010 admite L/W/H con L ≤ 2W. La caja sándwich conserva sus dos parámetros de origen y no introduce una altura ficticia. 102010 sigue pendiente de la topología de 92 cortes.

## Verificación local

`node comprobar-parametrizacion.cjs` comprueba:

- Identidad con la geometría original al introducir las medidas iniciales.
- Cambios en corte y pliegues al variar cada eje admitido.
- Conservación del número de caras y aberturas.
- Combinaciones de extremos de los modelos con rangos independientes y casos exactos de borde del material para FEFCO, con dimensiones finitas, extensión positiva y radios no negativos.
- Rechazo de medidas fuera del rango y valores no numéricos.

El resultado se guarda en `comprobacion-motores.json`. Estas comprobaciones no demuestran ausencia de intersecciones, ajuste de cierres, plegado 3D ni equivalencia completa con el sistema de referencia.

## Evidencia y limitaciones

Muestras originales en `../geometria/modelos/<código>/parametricas/`, con manifiestos de medidas, hashes y etapas. Evidencia REA:

- 150010: `ev_a18825c5a61e966696c553ba3647c52a8389a9bac182d10c9d2af4daad5a49bb`.
- 112047: `ev_cd90c934ef31fc36ebf2c28a9b1ea358996b3729433a3a73e679f52fc3f296a3`.
- 12109002: `ev_602b037b5204b8d18330691126ae1490b9ca509157ab98d0b3f27c281d6ec51d`.
- 112310: `ev_3d3f8c25ee3fcf3f0e6c3ce21115fc2c3d0e79b2ae3c7c53c6b47596e35185bd`.
- 10002003: `ev_da1553065cabada5c63e4a89bc115d334d059ff994b3da064b4b33ffde15041f`.
- 180370: `ev_9f15a6df8c23b64cf0650dd5bdfaa650770c22ebe822a4de8e305e2fccc72385`.

Las capturas anteriores devolvieron `cleanup_incomplete`: se conservaron las acciones completadas y las respuestas geométricas; el cierre correcto del navegador no quedó acreditado. Las variaciones de 10001006 y 180320 se capturaron después con Playwright; 10001006 quedó verificado y 180320 sigue pendiente de cerrar sus fórmulas.

`parametrizar-modelos.py` integra las reglas y los metadatos en el JSON autocontenido que utiliza el navegador. `preparar-datos.py` vuelve a aplicar esta integración cuando se regeneran los datos originales. El editor publicado utiliza únicamente sus datos locales.

## Ancho de material FEFCO 200010

El material es un pliego completo de **1.200 × 2.300 mm**. El ancho de 1.200 mm sigue siendo el límite duro de `totalX` en la orientación mostrada; la longitud de 2.300 mm limita la altura. La relación observada es `totalX = 44 + 2L + 2W` y `totalY = H + W + 2`. Con 434 × 144 × 278 mm el plano mide 1.200 × 424 mm y el editor calcula **5 cajas por pliego** (1 columna × 5 filas, sin giro). La yield usa **0 mm de sangría lateral** porque el plano ocupa exactamente los 1.200 mm del pliego; los planos comparten borde. La altura máxima para W=144 es 2.154 mm. Se mantienen mínimos L=30 y W=24 mm; los máximos de L/W se recalculan con la otra medida para no superar 1.200 mm. El generador rechaza cualquier plano que exceda el pliego y conserva la última geometría válida.

Las medidas iniciales del editor para este material son 434 × 144 × 278 mm; las medidas capturadas originales permanecen separadas para las reglas empíricas y las pruebas de identidad. El control de rango ampliado no se muestra para FEFCO, porque sus límites dependen del ancho del material. Los límites de fabricación y el rango de verificación empírica son conceptos separados.

## Pliego de la caja 10001029

Mínimos indicados por el usuario: L=15, W=10,6, H=15,6 mm. El troquel completo debe caber en 1.000 × 700 mm o en 700 × 1.000 mm girado. El motor valida ambas dimensiones y el panel muestra la orientación de encaje. Los máximos de cada campo se recalculan conservando las otras medidas, mediante las reglas de extensión del plano. El SVG conserva la orientación del lienzo; puede girarse al colocarlo en el pliego. Los rangos comprobados contra las capturas permanecen separados de estos límites físicos.

## Pliego de la caja 102010

Mínimos de referencia suministrados: L=15, W=10,6, H=20,6 mm; pliego 1.000 × 700 mm, admitiendo giro. Sigue activo únicamente el eje H: los cambios de L/W pueden modificar la topología del cierre snap-lock y no se dispone de una regla completa. Los mínimos de L/W se registran y muestran como referencia junto a los campos fijos, sin simular que son editables. Con L=120,6 y W=60,6 mm, la altura máxima para el pliego es 878,85 mm girando el plano. Se comprueban altura mínima, borde del pliego y rechazo de modificaciones de los ejes fijos.

## Límites adicionales de pliego

| Modelo | Mínimos L × W × H (mm) | Pliego (mm) |
|---|---|---|
| 150010 | 20 × 22 × 17,6 | 1.000 × 700 |
| 112047 | 30 × 30 × 30,6 | 1.000 × 700 |
| 12109002 | 30 × 30 × 30,6 | 1.000 × 700 |
| 112310 | 40 × 40 × 41 | 1.200 × 2.300 |
| 10001006 | 15 × 10,6 × 15,6 | 1.000 × 700 |
| 200010 | 30 × 24 × 20,6 | 1.200 × 2.300 |
| 187000 | 20 × 20 × 6,67 | 330 × 480 |
| 188060 | 20 × 20 × 20 (experimental) | no definido |

Se admite giro de 90°. Los límites de cada campo se recalculan con las otras medidas; el motor comprueba ambas dimensiones del plano antes de aceptar el cambio. Para 12109002, las dimensiones iniciales del editor son 200 × 140 × 120 mm: el plano resultante de 609,13 × 742,18 mm cabe girado. Su geometría capturada original permanece separada, ya que no cabe en el nuevo pliego. Estos límites de material sustituyen los rangos arbitrarios de exploración; no amplían la validación de la reconstrucción geométrica.

## Caja con ventana 15030101

Se retiró la transformación por zonas: deformaba pestañas, ranuras y radios y fallaba frente a las capturas originales. Se conserva la geometría exacta de cada material y espesor en 150 × 150 × 50 mm. Los mínimos solicitados (40 × 40 × 30 mm) quedan registrados como referencia; los ejes permanecen fijos hasta disponer de un generador fiel. No se considera validada la parametrización por comprobar únicamente medidas y conteos.

## Caja almohada 187000

Motor local `pillow187000`. Reconstruye corte, caras y pliegues con `x0 = H/2`, pestaña superior `y0 = 15` (18 mm para W ≥ 100), radio `R = (W²+H²)/(4H)` y muesca de cierre `rt = clamp(round((L+H)/25·2)/2, 6, 7,5)`. Extensión `totalX = L+H`, `totalY = 2W+y0`. Se validó contra 7 capturas del editor (error máximo 0,00007 mm en corte y 0,00003 mm en caras).

Rango editable: L 20–323,33 mm, W 20–231 mm, H 6,67–200 mm, con H < W. Pliego 330 × 480 mm; el motor comprueba el ajuste y el editor calcula las cajas por pliego con sangría de 3 mm y giro. Queda **verificado digitalmente** con 7 capturas (ver `validacion-parametrica.json`). No se verificó una exportación DXF/PDF ni una muestra física; revisa el armado antes de fabricar.

## Caja con fondo encajable 102010

Motor afín local para las tres medidas, ajustado con seis capturas de la topología de **80 cortes**. Error máximo observado: **1,82 mm** en los campos numéricos; la geometría base se reproduce exactamente. Los campos L, W y H son editables.

La restricción es **L ≤ 2W**. Por encima de esa relación el servidor cambia el fondo de 80 a **92 cortes** (12 comandos extra en HB/FB); esa segunda topología no está reconstruida y el editor la rechaza. El pliego es 1.000 × 700 mm y el motor comprueba el encaje. El modelo queda marcado como experimental: no se validó una muestra física.

## Caja hexagonal 188060

Motor de paneles L/W/H sobre la caja hexagonal de Pacdora: **100,6 × 40,6 × 181,6 mm** de base, cartón blanco de 0,5 mm, 19 caras, 26 pliegues y 28 cortes. `totalX = 135,5 + 2L`, `totalY = 2W + H`; los radios se conservan. Base exacta y L=110 validado con error máximo 0,7 mm. W=45 y H=190 se validaron con errores de 0,16 mm y 0,00 mm; L=110 tiene 0,70 mm. Queda experimental: el error máximo es 0,70 mm en L; faltan muestras independientes de W/H, la muesca exacta y validación física. La miniatura es el mockup oficial de Pacdora.

## Caja para tarta con ventana 15030101

Motor afín L/W/H experimental para la topología grande (129 cortes/18 pliegues). Se ajustó con seis muestras; la base es exacta y el error máximo es **3,88 mm** en `totalX`. Límites: L/W ≥ 100 mm y H ≥ 30 mm. Por debajo de L/W 100 cambia la topología a 113 cortes/16 pliegues, que no está reconstruida. Sin validación física.

## Caja rígida 366010

Motor `rigid366010` de cuatro capas (cartón gris y papel de fondo/tapa). Se capturaron 58 configuraciones en L 160–220 mm, W 80–140 mm, H 30–70 mm; el ajuste es afín por régimen (A: L < 200; B: L ≥ 200 con profundidad exterior variable). Error máximo **0,000 mm** fuera de `/bleeds`; el sangrado dibujado se recalcula a 3 mm del corte. Queda **verificado digitalmente**; la validación física y la ampliación de rango siguen pendientes. Uso y límites en `geometria/modelos/366010/README.md`.
