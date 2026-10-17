[Español](README.md) · English

# Pacdora · Dieline Workshop

Local dieline application, geometric models, and research into Pacdora boxes.

## Structure

| Directory | Contents |
|---|---|
| `editor-troqueles/` | Main application, assets, translations, tests, and data preparation |
| `geometria/` | Models, geometric responses, generators, icons, and technical sheets |
| `investigacion/` | Materials research, interface research, and editor screenshots |
| `evidencias/` | Original REA captures and large bundles; retained locally and excluded from Git |
| `archivo/` | Previous copies, ZIP packages, and previous Git histories; excluded from Git |
| `docs/` | General analysis and the reorganization move log |
| `scripts/` | Project checks and utilities |
| `skills/` | Reusable `obtener CODIGO` workflow |
| `dist` | Link to `editor-troqueles/dist`, without duplicating the application |

## Run

From the project root:

```sh
python3 -m http.server 8000 --directory editor-troqueles/dist
```

Open http://localhost:8000/.

```sh
node --test editor-troqueles/tests/*.test.cjs
```

To acquire a box in this project, enter `obtener 15030101` in the chat. Instructions are in [the skill](skills/obtener-pacdora/SKILL.en.md).

## Research and traceability

Original REA records are not edited when reorganized. Their historical paths may refer to the previous location; [the move log](docs/organizacion-movimientos.json) identifies the current files. Research scripts that work with the publication copy point to `archivo/copias/boxcraft-publicacion`; they are separate from the main application's preparation process.

Large captures and archived histories will not be included when files are added to the new repository. Back them up separately when moving the project to another computer.

The editor's previous history is retained in `archivo/historial/editor-troqueles.git`. Inspect it from the root:

```sh
git --git-dir=archivo/historial/editor-troqueles.git --work-tree=editor-troqueles log --oneline
```

The publication copy retains its own history in `archivo/copias/boxcraft-publicacion/.git`. The reorganization creates no commits and configures no remote for the root repository.

## Documentation languages

Spanish documents remain unchanged. English companions use the `.en.md` suffix and retain technical paths, commands, and evidence references. Archived copies have their own English companions as well.

| Document | Original | English |
|---|---|---|
| `AGENTS.md` | [Original](AGENTS.md) | [English](AGENTS.en.md) |
| `README.md` | [Original](README.md) | [English](README.en.md) |
| `archivo/copias/boxcraft-publicacion/INTERNACIONALIZACION.md` | [Original](archivo/copias/boxcraft-publicacion/INTERNACIONALIZACION.md) | [English](archivo/copias/boxcraft-publicacion/INTERNACIONALIZACION.en.md) |
| `archivo/copias/boxcraft-publicacion/MATERIALES.md` | [Original](archivo/copias/boxcraft-publicacion/MATERIALES.md) | [English](archivo/copias/boxcraft-publicacion/MATERIALES.en.md) |
| `archivo/copias/boxcraft-publicacion/PARAMETRIZACION.md` | [Original](archivo/copias/boxcraft-publicacion/PARAMETRIZACION.md) | [English](archivo/copias/boxcraft-publicacion/PARAMETRIZACION.en.md) |
| `archivo/copias/boxcraft-publicacion/README.md` | [Original](archivo/copias/boxcraft-publicacion/README.md) | [English](archivo/copias/boxcraft-publicacion/README.en.md) |
| `archivo/copias/boxcraft/INTERNACIONALIZACION.md` | [Original](archivo/copias/boxcraft/INTERNACIONALIZACION.md) | [English](archivo/copias/boxcraft/INTERNACIONALIZACION.en.md) |
| `archivo/copias/boxcraft/MATERIALES.md` | [Original](archivo/copias/boxcraft/MATERIALES.md) | [English](archivo/copias/boxcraft/MATERIALES.en.md) |
| `archivo/copias/boxcraft/PARAMETRIZACION.md` | [Original](archivo/copias/boxcraft/PARAMETRIZACION.md) | [English](archivo/copias/boxcraft/PARAMETRIZACION.en.md) |
| `archivo/copias/boxcraft/README.md` | [Original](archivo/copias/boxcraft/README.md) | [English](archivo/copias/boxcraft/README.en.md) |
| `docs/analisis-pacdora.md` | [Original](docs/analisis-pacdora.md) | [English](docs/analisis-pacdora.en.md) |
| `editor-troqueles/INTERNACIONALIZACION.md` | [Original](editor-troqueles/INTERNACIONALIZACION.md) | [English](editor-troqueles/INTERNACIONALIZACION.en.md) |
| `editor-troqueles/MATERIALES.md` | [Original](editor-troqueles/MATERIALES.md) | [English](editor-troqueles/MATERIALES.en.md) |
| `editor-troqueles/PARAMETRIZACION.md` | [Original](editor-troqueles/PARAMETRIZACION.md) | [English](editor-troqueles/PARAMETRIZACION.en.md) |
| `editor-troqueles/README.md` | [Original](editor-troqueles/README.md) | [English](editor-troqueles/README.en.md) |
| `editor-troqueles/investigacion-materiales/README.md` | [Original](editor-troqueles/investigacion-materiales/README.md) | [English](editor-troqueles/investigacion-materiales/README.en.md) |
| `editor-troqueles/investigacion-materiales/matriz-validacion.md` | [Original](editor-troqueles/investigacion-materiales/matriz-validacion.md) | [English](editor-troqueles/investigacion-materiales/matriz-validacion.en.md) |
| `geometria/README-modelo.md` | [Original](geometria/README-modelo.md) | [English](geometria/README-modelo.en.md) |
| `geometria/modelos/10001006/README.md` | [Original](geometria/modelos/10001006/README.md) | [English](geometria/modelos/10001006/README.en.md) |
| `geometria/modelos/10001029/README.md` | [Original](geometria/modelos/10001029/README.md) | [English](geometria/modelos/10001029/README.en.md) |
| `geometria/modelos/10002003/README.md` | [Original](geometria/modelos/10002003/README.md) | [English](geometria/modelos/10002003/README.en.md) |
| `geometria/modelos/102010/README.md` | [Original](geometria/modelos/102010/README.md) | [English](geometria/modelos/102010/README.en.md) |
| `geometria/modelos/112047/README.md` | [Original](geometria/modelos/112047/README.md) | [English](geometria/modelos/112047/README.en.md) |
| `geometria/modelos/112310/README.md` | [Original](geometria/modelos/112310/README.md) | [English](geometria/modelos/112310/README.en.md) |
| `geometria/modelos/12109002/README.md` | [Original](geometria/modelos/12109002/README.md) | [English](geometria/modelos/12109002/README.en.md) |
| `geometria/modelos/150010/README.md` | [Original](geometria/modelos/150010/README.md) | [English](geometria/modelos/150010/README.en.md) |
| `geometria/modelos/15030101/MATERIALES.md` | [Original](geometria/modelos/15030101/MATERIALES.md) | [English](geometria/modelos/15030101/MATERIALES.en.md) |
| `geometria/modelos/15030101/README.md` | [Original](geometria/modelos/15030101/README.md) | [English](geometria/modelos/15030101/README.en.md) |
| `geometria/modelos/180320/README.md` | [Original](geometria/modelos/180320/README.md) | [English](geometria/modelos/180320/README.en.md) |
| `geometria/modelos/180370/README.md` | [Original](geometria/modelos/180370/README.md) | [English](geometria/modelos/180370/README.en.md) |
| `geometria/ruta-conversion-3d.md` | [Original](geometria/ruta-conversion-3d.md) | [English](geometria/ruta-conversion-3d.en.md) |
| `investigacion/interfaz-150010/analisis.md` | [Original](investigacion/interfaz-150010/analisis.md) | [English](investigacion/interfaz-150010/analisis.en.md) |
| `investigacion/materiales/INFORME.md` | [Original](investigacion/materiales/INFORME.md) | [English](investigacion/materiales/INFORME.en.md) |
| `investigacion/materiales/physical-fit-findings.md` | [Original](investigacion/materiales/physical-fit-findings.md) | [English](investigacion/materiales/physical-fit-findings.en.md) |
| `skills/obtener-pacdora/SKILL.md` | [Original](skills/obtener-pacdora/SKILL.md) | [English](skills/obtener-pacdora/SKILL.en.md) |

## Deployment

GitHub Pages: https://dospuntocero.github.io/boxcraft/

The `Publish GitHub Pages` workflow runs tests and publishes **`editor-troqueles/dist/`** from `main` to the root of `gh-pages`. In Settings → Pages, keep **Deploy from a branch → gh-pages → /(root)**. It can also be run manually with `workflow_dispatch`. The root `dist` symlink and research folders are not deployment inputs.

Sites: https://taller-troqueles-fran.happyjay2.chatgpt.site/ uses the same application directory. Source synchronization and deployment run separately with the Sites helper.
