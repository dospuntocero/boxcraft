# Parametrización de los ocho modelos que tenían medidas fijas

Los ocho modelos ya tienen generadores locales. La selección, los campos de medidas, la conversión mm/in, las capas y el SVG usan la misma geometría generada. El material y el espesor siguen fijos.

| Modelo | Ejes nuevos | Método | Alcance |
|---|---|---|---|
| 150010 · Mailer | L/W/H | Reglas por coordenada obtenidas de variaciones de dimensiones | Dos muestras adicionales coinciden en los 1.297 campos numéricos; rango observado 315–330 / 202–212 / 62–66 mm |
| 112047 · Techo y cordón | L/W/H | Reglas empíricas por coordenada | Experimental; diferencia máxima de 1,75 en los campos numéricos de las muestras de comprobación |
| 12109002 · Pastel | L/W/H | Reglas empíricas por coordenada | Experimental; diferencia máxima 1,574 |
| 112310 · Asa y fondo | L/W/H | Reglas empíricas por coordenada | Experimental; diferencia máxima 2,5 |
| 10001006 · Solapas | L/W/H | Transformación por paneles, con tira de pegado y lengüetas terminales fijas | Reconstrucción experimental; sin comprobación con variaciones del original |
| 10002003 · Colgar | L/W/H | Reglas empíricas por coordenada | Experimental; diferencia máxima 0,5 |
| 180370 · Papas fritas | L/W/H | Reglas empíricas por coordenada, conservando arcos | Experimental; diferencia máxima 0,536 |
| 180320 · Sándwich | L/W | Transformación por paneles y diagonales | Reconstrucción experimental; sin comprobación con variaciones del original |

Las diferencias anteriores incluyen todos los campos numéricos del plano, no son una tolerancia física de fabricación. Los campos de coordenadas y longitudes están en mm. Los valores completos están en `validacion-parametrizacion.json`. No se presenta una comparación fallida como validación aprobada.

Los motores experimentales ofrecen adaptación de la geometría, pero no reproducen todos los ajustes automáticos y redondeos del servicio original. Se señalan en el catálogo y el panel de medidas. El rango ampliado de estos ocho modelos es 75–150 % de cada medida original; fuera del rango observado, incluso 150010 se identifica como experimental. Se necesita una muestra física para confirmar el armado.

Los tres modelos que ya eran editables mantienen sus reglas: 200010 y 10001029 admiten L/W/H; 102010 conserva la edición solo de altura. La caja sándwich conserva sus dos parámetros de origen y no introduce una altura ficticia.

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

Las capturas anteriores devolvieron `cleanup_incomplete`: se conservaron las acciones completadas y las respuestas geométricas; el cierre correcto del navegador no quedó acreditado. Las capturas de variaciones de 10001006 y 180320 no se completaron. Sus reglas se diseñaron a partir de los paneles y pliegues del plano inicial; no se atribuyen al código original.

`parametrizar-modelos.py` integra las reglas y los metadatos en el JSON autocontenido que utiliza el navegador. `preparar-datos.py` vuelve a aplicar esta integración cuando se regeneran los datos originales. El editor publicado utiliza únicamente sus datos locales.

## Ancho de material FEFCO 200010

El límite físico configurado es 1.200 mm para `totalX` del plano desplegado, en la orientación mostrada. No se aplica rotación automática. La relación observada es `totalX = 44 + 2L + 2W`; los máximos del formulario se recalculan con la otra medida. La altura tiene mínimo 20,6 mm y no tiene máximo de largo de material configurado. Se mantienen mínimos L=30 y W=24 mm. El generador rechaza cualquier plano que exceda 1.200 mm y conserva la última geometría válida.

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

Se admite giro de 90°. Los límites de cada campo se recalculan con las otras medidas; el motor comprueba ambas dimensiones del plano antes de aceptar el cambio. Para 12109002, las dimensiones iniciales del editor son 200 × 140 × 120 mm: el plano resultante de 609,13 × 742,18 mm cabe girado. Su geometría capturada original permanece separada, ya que no cabe en el nuevo pliego. Estos límites de material sustituyen los rangos arbitrarios de exploración; no amplían la validación de la reconstrucción geométrica.
