# Generador local FEFCO 0201

Ejecutar desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelo-parametrico.py --length 457.2 --width 228.6 --height 279.4
```

Produce troquel-generado.svg y troquel-generado.json en este directorio. Las medidas son de manufactura y están expresadas en milímetros. Funciona sin red ni bibliotecas externas. Cada ejecución reconstruye las reglas desde las capturas locales y comprueba la combinación independiente antes de generar el archivo. Reemplaza los archivos de salida anteriores.

Rangos admitidos: largo 434–508 mm, ancho 214–254 mm, alto 278–304.8 mm. Material fijo: Onda B, espesor 3 mm, OF=2, R=3, G=45 y GT=15. No representa otros espesores ni cambios manuales de parámetros avanzados.

Es un modelo empírico afín: aplica a cada campo numérico de la geometría las variaciones observadas en tres muestras, una por eje. No es el código original de Pacdora. La combinación independiente 457.2 × 228.6 × 279.4 mm no se usa para ajustar las reglas y valida 822 campos numéricos. Se toleran únicamente diferencias de sangría inferiores a 0.001 mm; las otras diferencias numéricas deben estar dentro de 0.000001 unidades. El archivo validacion-modelo.json registra el resultado completo.

## Reglas resumidas observadas

Con L, W y H de manufactura, y la configuración fija anterior:

- Extensión del plano: X=45+2L+2W−1; Y=H+W+2.
- Solapas: F=W/2+1; F1=W/2+3.
- Caras principales: anchos L, W, L y W−1, en ese orden.
- Pestaña de pegado: ancho 45; altura de metadatos H−4.
- Medidas internas: L−4, W−4, H−8.
- Medidas externas: L+2, W+2, H+4.

Estas relaciones coinciden con las muestras inspeccionadas. No demuestran que se mantengan fuera del rango, con otro material o después de modificar parámetros avanzados. Los contornos y arcos se generan a partir de coeficientes por campo, conservados en reglas-parametricas.json.

## Archivos y procedencia

- experimentos/: muestras individuales de L, W, H y espesor, y manifiesto con etapas, hashes y estados.
- validacion-parametrica/: muestras de comprobación independientes; la final es knife-04.json.
- reglas-parametricas.json: plantilla y coeficientes aprendidos exclusivamente de las muestras individuales de dimensiones.
- modelo-parametrico.py: ajuste, validación y salida SVG/JSON.

Evidencia de las muestras: ev_70c78216d8ca163ef7f939d0aed16da00ebc22365fb62afe71f36c34f435b46a. Evidencia de comprobación: ev_e71c55c541c5bd0970f35ad5e7d9e8acfe58b97439dd0975c40c6f3260455e65. Ambas capturas reportaron cleanup_incomplete: el registro parcial conserva todas las acciones completadas y las respuestas concretas usadas, pero no acredita cierre correcto del navegador. No se presenta su ciclo de vida como completo.

La pestaña avanzada observada en ev_f5a6bc57aa5f99256bd933eac5f9a8ebfa1cfaf1ca8187ee3166b635309300bf exige «Actualizar a Negocios». No se modificaron esos parámetros ni se intentó eludir la restricción.

El SVG incluye colores de inspección para caras, corte y pliegue. No se exporta sangría, no se verificaron arcos mediante comparación visual y no está validado para fabricación. Antes de ampliar el motor hacen falta más combinaciones, cambios de parámetros autorizados, verificación visual y una muestra física.
