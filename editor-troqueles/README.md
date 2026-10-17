# Boxcraft

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

GitHub Pages se publica mediante `.github/workflows/pages.yml` desde la raíz del repositorio: las fuentes están en `editor-troqueles/dist/` y la salida se envía a `gh-pages`. No copiar la aplicación a `docs/`, que contiene documentación.

Los catálogos de modelos y materiales incluyen restricciones de edición y compatibilidad. Comprobar el armado con una muestra antes de fabricar.
