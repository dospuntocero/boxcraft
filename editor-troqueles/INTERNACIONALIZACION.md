# Traducciones del frontend

La interfaz admite español e inglés. Los botones de banderas guardan la preferencia en `localStorage` (`taller.language`). En la primera visita se utiliza el idioma del navegador si está disponible y español como alternativa.

- `dist/locales/es.js` y `dist/locales/en.js`: catálogos. Las frases originales son claves estables al estilo gettext.
- `dist/i18n.js`: traducción, interpolación de `{parametros}`, formato regional y actualización del documento.
- HTML: usar `data-i18n` para texto y `data-i18n-aria-label`, `data-i18n-title`, `data-i18n-alt`, `data-i18n-placeholder` o `data-i18n-content` para atributos. Aplicar la clave a un elemento que solo contenga texto para conservar iconos y controles.
- JavaScript: usar `I18n.t(clave, parametros)` en cada texto visible, mensaje de error y etiqueta de accesibilidad. Preferir mensajes completos con parámetros para textos nuevos.
- Datos: `I18n.fields` traduce nombres de modelos, nombres y grupos de materiales y motivos de incompatibilidad mediante getters; los identificadores, categorías internas, rutas y valores geométricos siguen siendo estables.
- Números visibles: usar `I18n.locale`. Los valores de inputs y coordenadas SVG conservan el formato numérico requerido por el navegador.

Al cambiar de idioma se actualizan el documento, los paneles y el SVG sin recargar la página. Se conservan el modelo, las dimensiones confirmadas, el material, las unidades, las capas y la posición del lienzo.

Para añadir un idioma, crear su catálogo con todas las claves del español, cargarlo antes de `i18n.js`, registrarlo en `supported`, definir su región en `locale` y añadir un botón con `data-language` al grupo de banderas. Mantener sincronizadas las distribuciones `editor-troqueles/dist` y `../dist`.

Validación desde `editor-troqueles`: `node --test tests/*.test.cjs`. Las pruebas de i18n comprueban cobertura de claves y datos, cambio de idioma, mensajes de validación, persistencia y alternativas.
