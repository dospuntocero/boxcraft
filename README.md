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

## Publicar

Configurar `dist/` como directorio público del servidor de archivos estáticos. Se debe conservar su estructura completa.

Para una publicación manual con GitHub Pages, copiar el contenido de `dist/` a la carpeta `docs/` del repositorio y seleccionar la rama `main` y la carpeta `/docs` en Settings → Pages. La aplicación utiliza rutas relativas y puede funcionar bajo el nombre del repositorio.

Los catálogos de modelos y materiales incluyen restricciones de edición y compatibilidad. Comprobar el armado con una muestra antes de fabricar.
