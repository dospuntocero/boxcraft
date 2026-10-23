# Materiales y espesores

La aplicación muestra únicamente combinaciones de material, espesor y medidas que tienen geometría disponible. Los materiales que no tienen una combinación válida para las medidas y el modo de tamaño actuales se ocultan. Si queda un solo material, se oculta el selector y su nombre se muestra junto al espesor.

El espesor utiliza valores discretos observados y depende del material. Las nuevas geometrías son capturas exactas, con sus compensaciones internas y externas; no se interpolan ni se escalan entre espesores. La edición paramétrica anterior se conserva para el material y espesor originales. En las nuevas combinaciones, las medidas son fijas y la interfaz indica este alcance.

La caja **366010** es una excepción controlada: mantiene un único material (cartón gris + papel de 0,15 mm) y habilita cinco espesores discretos de cartón (1,5; 1,75; 2; 2,25; 2,5 mm), cada uno con su propia plantilla base. No se interpola entre espesores ni se extrapola fuera de ese intervalo; la edición L/W/H sigue activa dentro del rango verificado.

## Cobertura de geometrías adicionales

| Modelo | Materiales adicionales observados | Combinaciones adicionales de material y espesor |
|---|---:|---:|
| 200010 — Caja de envío FEFCO | 1 | 2 |
| 102010 — Caja con fondo encajable | 1 | 8 |
| 150010 — Caja mailer con tapa | 9 | 16 |
| 112047 — Caja con techo y cordón | 7 | 7 |
| 12109002 — Caja para pastel | 0 | 0 |
| 112310 — Caja con asa y fondo | 9 | 9 |
| 10001006 — Estuche con solapas | 2 | 6 |
| 10002003 — Estuche para colgar | 2 | 3 |
| 180370 — Envase para papas fritas | 2 | 3 |
| 180320 — Caja sándwich con ventana | 2 | 3 |
| 187000 — Caja almohada | 2 | 2 |

## Límites de la revisión

La caja 12109002 conserva su material original: no se completó la verificación de alternativas. La fuente de referencia devolvió HTTP 403 durante las capturas y dejó los controles deshabilitados. También quedan sin validar los intervalos continuos de espesor y la edición libre de dimensiones para los nuevos materiales. Un material oculto significa que no hay una configuración habilitada en la aplicación; no demuestra incompatibilidad física para todos los posibles tamaños.

En 187000, el cartón blanco de 210 g y el kraft de 190 g reproducen exactamente el corte del material original; se habilitaron reutilizando su capa y con las medidas fijas. En 188060 el corte cambia con el material: Onda E modifica el ancho del plano y las compensaciones, por lo que sigue pendiente de captura material por material.

Las respuestas y la investigación completas se conservan localmente. Cada geometría adicional incluye una referencia a la captura (identificador REA cuando estuvo disponible) y un SHA-256 de su respuesta. Las pruebas cubren el cambio real de trazado, los límites, las conversiones y el rechazo de combinaciones fuera de las medidas comprobadas.
