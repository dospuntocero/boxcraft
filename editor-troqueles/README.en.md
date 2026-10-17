[Español](README.md) · English

# Boxcraft

Web application for browsing a box library, editing dimensions, and downloading SVG blanks with cutting, folding, bleed, and dimension lines.

Includes Spanish and English interfaces, a language selector with flags, and a preference saved in the browser.

## Run locally

No dependency installation or build is required. From the project directory:

```sh
python3 -m http.server 8000
```

Open http://localhost:8000/dist/ in your browser. Files must be served over HTTP to load JSON catalogs.

## Structure

- `dist/`: complete application ready to serve, including JavaScript, styles, translations, data, and images.
- `tests/`: geometric engine, materials, and internationalization tests.
- `INTERNACIONALIZACION.md`: instructions for maintaining and extending translations; [English version](INTERNACIONALIZACION.en.md).
- `PARAMETRIZACION.md`: model parameterization documentation; [English version](PARAMETRIZACION.en.md).

## Tests

Require Node.js 18 or later:

```sh
node --test tests/*.test.cjs
```

## Publishing

Configure `dist/` as the static file server's public directory. Preserve its full structure.

For manual publication with GitHub Pages, copy the contents of `dist/` into the repository's `docs/` directory and select the `main` branch and `/docs` folder in Settings → Pages. The application uses relative paths and can run under the repository name.

Model and material catalogs include editing and compatibility restrictions. Check assembly with a sample before manufacturing.
