# boxcraft
An open-source, box dielinemaker editor written by scratch in pure js

## Dieline maker for the rest of us
Small selection of currently used boxes. multilingual and super fast

Aplicación web para explorar una biblioteca de cajas, editar sus dimensiones y descargar planos SVG con líneas de corte, pliegue, sangrado y cotas.

Incluye interfaz en español e inglés, selector de idioma con banderas y preferencia guardada en el navegador.

## Ejecutar localmente

No requiere instalar dependencias ni compilar. Desde la carpeta del proyecto:

```sh
python3 -m http.server 8000
```

Abrir http://localhost:8000/dist/ en el navegador. Es necesario servir los archivos por HTTP para cargar los catálogos JSON.

## Estructura

- `dist/`: aplicación completa lista para servir, incluyendo código JavaScript, estilos, traducciones, datos e imágenes.
- `tests/`: pruebas del motor geométrico, materiales e internacionalización.
- `INTERNACIONALIZACION.md`: instrucciones para mantener y ampliar las traducciones.
- `PARAMETRIZACION.md`: documentación de la parametrización de modelos.

## Pruebas

Requieren Node.js 18 o posterior:

```sh
node --test tests/*.test.cjs
```

## Sitio público

La aplicación está disponible en https://dospuntocero.github.io/boxcraft/.

## Publicar actualizaciones

GitHub Pages sirve la rama `gh-pages`, cuyo contenido es exclusivamente la carpeta `dist/` de `main`. Después de confirmar los cambios:

```sh
git push origin main
git subtree push --prefix dist origin gh-pages
```

También se puede configurar `dist/` como directorio público en otro servidor estático, conservando su estructura completa.

Los catálogos de modelos y materiales incluyen restricciones de edición y compatibilidad. Comprobar el armado con una muestra antes de fabricar.

## Materiales y espesores

Consulta [MATERIALES.md](MATERIALES.md) para conocer la compatibilidad habilitada, las medidas comprobadas y las limitaciones de las nuevas geometrías. El selector de material desaparece cuando solo existe una opción válida.
