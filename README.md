# Pacdora · Taller de troqueles

Aplicación local de troqueles, modelos geométricos e investigación de cajas de Pacdora.

## Estructura

| Carpeta | Contenido |
|---|---|
| `editor-troqueles/` | Aplicación principal, assets, traducciones, pruebas y preparación de datos |
| `geometria/` | Modelos, respuestas geométricas, generadores, iconos y fichas técnicas |
| `investigacion/` | Investigación de materiales, interfaz y capturas del editor |
| `evidencias/` | Capturas originales REA y bundles pesados; conservados localmente, excluidos de Git |
| `docs/` | Análisis general y registro de movimientos de la reorganización |
| `scripts/` | Comprobaciones y utilidades del proyecto |
| `skills/` | Flujo reutilizable `obtener CODIGO` |
| `dist` | Enlace a `editor-troqueles/dist`, sin duplicar la aplicación |

## Ejecutar

Desde la raíz:

```sh
python3 -m http.server 8000 --directory editor-troqueles/dist
```

Abrir http://localhost:8000/.

```sh
node --test editor-troqueles/tests/*.test.cjs
```

Para adquirir una caja en este proyecto, escribir en el chat `obtener 15030101`. Las instrucciones están en [la skill](skills/obtener-pacdora/SKILL.md).

## Investigación y trazabilidad

Los registros originales REA conservan rutas históricas. El [registro de movimientos](docs/organizacion-movimientos.json) documenta la reorganización anterior; sus referencias son históricas, no dependencias actuales. Las copias archivadas y los historiales Git locales anteriores se han eliminado.

La aplicación vigente está en `editor-troqueles/`. Los generadores de escenarios de investigación leen sus catálogos. Los generadores de perfiles físicos y observados escriben candidatos en `investigacion/materiales/physical-profiles.json` y `observed-profiles.json`; no sobrescriben las capacidades de la aplicación.

El repositorio raíz conserva el historial de GitHub y utiliza `dospuntocero/boxcraft` como `origin`. Las capturas pesadas de `evidencias/` están excluidas de Git y deben respaldarse por separado si se mueve el proyecto a otro equipo.

## Publicación

GitHub Pages: https://dospuntocero.github.io/boxcraft/

El workflow `Publish GitHub Pages` ejecuta las pruebas y publica **`editor-troqueles/dist/`** desde `main` en la raíz de `gh-pages`. En Settings → Pages se mantiene **Deploy from a branch → gh-pages → /(root)**. También puede ejecutarse manualmente con `workflow_dispatch`. El enlace `dist` de la raíz y las carpetas de investigación no son entradas de publicación.

Sites: https://taller-troqueles-fran.happyjay2.chatgpt.site/ utiliza la misma aplicación. La sincronización de fuentes y el deploy se realizan por separado con el helper de Sites.
