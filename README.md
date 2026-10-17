# Pacdora · Taller de troqueles

Aplicación local de troqueles, modelos geométricos e investigación de cajas de Pacdora.

## Estructura

| Carpeta | Contenido |
|---|---|
| `editor-troqueles/` | Aplicación principal, assets, traducciones, pruebas y preparación de datos |
| `geometria/` | Modelos, respuestas geométricas, generadores, iconos y fichas técnicas |
| `investigacion/` | Investigación de materiales, interfaz y capturas del editor |
| `evidencias/` | Capturas originales REA y bundles pesados; conservados localmente, excluidos de Git |
| `archivo/` | Copias anteriores, paquetes ZIP e historiales Git anteriores; excluidos de Git |
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

Los registros originales REA no se editan al reorganizarlos. Sus rutas históricas pueden referirse a la ubicación anterior; [el registro de movimientos](docs/organizacion-movimientos.json) permite localizar los archivos actuales. Los scripts de investigación que trabajan con la copia de publicación apuntan a `archivo/copias/boxcraft-publicacion`; no son el proceso de preparación de la aplicación principal.

Las capturas pesadas y los historiales archivados no se incluirán al añadir archivos al nuevo repositorio. Deben respaldarse por separado si se mueve el proyecto a otro equipo.

El historial anterior del editor se conserva en `archivo/historial/editor-troqueles.git`. Puede consultarse desde la raíz:

```sh
git --git-dir=archivo/historial/editor-troqueles.git --work-tree=editor-troqueles log --oneline
```

La copia de publicación conserva su propio historial dentro de `archivo/copias/boxcraft-publicacion/.git`. El repositorio raíz continúa el historial de `dospuntocero/boxcraft` y tiene configurado ese remoto como `origin`.

## Publicación

GitHub Pages: https://dospuntocero.github.io/boxcraft/

El workflow `Publish GitHub Pages` ejecuta las pruebas y publica **`editor-troqueles/dist/`** desde `main` en la raíz de `gh-pages`. En Settings → Pages se mantiene **Deploy from a branch → gh-pages → /(root)**. También puede ejecutarse manualmente con `workflow_dispatch`. El enlace `dist` de la raíz y las carpetas de investigación no son entradas de publicación.

Sites: https://taller-troqueles-fran.happyjay2.chatgpt.site/ utiliza la misma aplicación. La sincronización de fuentes y el deploy se realizan por separado con el helper de Sites.
