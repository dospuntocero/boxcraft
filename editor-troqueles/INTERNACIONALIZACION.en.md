[Español](INTERNACIONALIZACION.md) · English

# Frontend translations

The interface supports Spanish and English. Flag buttons save the preference in `localStorage` (`taller.language`). On the first visit, the browser language is used when available, with Spanish as the fallback.

- `dist/locales/es.js` and `dist/locales/en.js`: catalogs. Original phrases are stable gettext-style keys.
- `dist/i18n.js`: translation, `{parametros}` interpolation, regional formatting, and document updates.
- HTML: use `data-i18n` for text and `data-i18n-aria-label`, `data-i18n-title`, `data-i18n-alt`, `data-i18n-placeholder`, or `data-i18n-content` for attributes. Apply the key to an element containing only text to preserve icons and controls.
- JavaScript: use `I18n.t(clave, parametros)` for every visible string, error message, and accessibility label. Prefer complete parameterized messages for new text.
- Data: `I18n.fields` translates model names, material names and groups, and incompatibility reasons through getters; identifiers, internal categories, paths, and geometric values remain stable.
- Visible numbers: use `I18n.locale`. Input values and SVG coordinates retain the numeric format required by the browser.

Changing language updates the document, panels, and SVG without reloading the page. The model, confirmed dimensions, material, units, layers, and canvas position are preserved.

To add a language, create its catalog with every Spanish key, load it before `i18n.js`, register it in `supported`, define its region in `locale`, and add a `data-language` button to the flag group. Keep the `editor-troqueles/dist` and `../dist` distributions synchronized.

Validation from `editor-troqueles`: `node --test tests/*.test.cjs`. The i18n tests check key and data coverage, language changes, validation messages, persistence, and fallbacks.
