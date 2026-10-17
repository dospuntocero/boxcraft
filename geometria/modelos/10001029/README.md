# Caja para loción corporal · 10001029

Fuente: https://www.pacdora.com/es/dielines-detail/body-lotion-box-dieline-10001029

Se capturó un troquel plegable de familia `Pair`, con 13 caras, 76 comandos de corte y 12 pliegues. La configuración inicial es 60 × 45 × 120 mm de manufactura, cartón blanco 350 g y espesor 0.5 mm. La superficie del plano inicial ocupa 222.5 × 235 mm.

## Resultados

- troquel-base.svg: representación del plano original capturado, 60 × 45 × 120 mm.
- troquel-generado.svg: reconstrucción local, por defecto 68.58 × 53.34 × 139.7 mm.
- troquel-generado.json: geometría generada sin red.
- reglas.json: coeficientes y plantilla, obtenidos de 8 muestras de entrenamiento.
- validacion-generador.json: comparación contra 3 respuestas independientes, excluidas del ajuste.
- muestras/, ajustes/ y validacion/: respuestas y manifiestos de REA con etapas y hashes.

## Ejecutar

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/10001029/generar.py --length 70 --width 55 --height 140
```

Reemplaza troquel-generado.svg y troquel-generado.json en esta carpeta. Python estándar, sin dependencias ni consultas a Pacdora. Las medidas son de manufactura en mm. Se admite L=68.58–76.2, W=45–63.5 y H=120–152.4, con el material y espesor originales. El plano de 60 × 45 × 120 mm se conserva como captura; ese largo queda fuera del intervalo del generador porque pertenece a otra rama de valores automáticos.

## Cómo se reconstruyó

Las muestras individuales fueron L=76.2, W=63.5 y H=152.4 respecto de la base 60 × 45 × 120. Se añadieron L=70 y W=50,55,60 para separar los ajustes automáticos. Los contornos se modelaron como funciones afines de L,W,H y de tres valores internos E,A,AR.

No se exponen controles avanzados. Los valores automáticos son necesarios para reproducir el comportamiento de los controles básicos: en la rama admitida E=8 y S=6; las fórmulas inferidas A=floor(min(L/2,0.65W)) y AR=max(7,floor(0.15W)) coinciden con las muestras inspeccionadas. Estas fórmulas son inferencias acotadas, no recuperación del código original ni demostración de todos sus umbrales.

Comprobaciones independientes:

| L × W × H, mm | Campos numéricos comparados | Resultado |
| --- | --- | --- |
| 68.58 × 45 × 120 | 784 | Coinciden dentro de 0.000001 unidades |
| 68.58 × 53.34 × 120 | 784 | Coinciden dentro de 0.000001 unidades |
| 68.58 × 53.34 × 139.7 | 784 | Coinciden dentro de 0.000001 unidades |

Los tres estados pertenecen a una captura independiente. No son tres sesiones independientes. La caja delimitada por los rangos no se verificó exhaustivamente. La sangría no se genera: su ajuste inicial mostró desviaciones de hasta 0.0045823 mm y se excluyó del modelo final, comparación y salida. Se excluyeron también anotaciones sizeArrowData, que no se representan en el SVG.

Los arcos usan los campos originales en comandos SVG A. Se comprobó la sintaxis XML, pero no la equivalencia visual con el editor ni una muestra física. El SVG contiene colores de inspección y no está validado para fabricación.

## Evidencia

- Inspección inicial: ev_e3efff917250484126939187e1645d372d2628e3b319ed45df287669f241196f.
- Muestras: ev_4372b6a27b21d7713b101585d6645366f184b5b625ed9e15d73b6c30f52f9a8c.
- Ajustes: ev_72b528c47cfcd19649fe1797a2ba81c62a81da3f9359c0ea3a0e0006ccbdc452.
- Comprobación independiente: ev_d5b586b9829507684a1c975a9d86fb0e734ef0326bb860329189afdbc5e937ef.

Las capturas de muestras y ajustes reportaron cleanup_incomplete; se recuperaron sus observaciones parciales conservadas. Las acciones registradas se completaron y las respuestas usadas están presentes. La captura de comprobación se completó, pero excedió el límite de transporte; se recuperó mediante exportación sin repetirla. Estas limitaciones no se omiten al interpretar los datos.
