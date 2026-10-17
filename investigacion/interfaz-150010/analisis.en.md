[Español](analisis.md) · English

# Analysis of the Pacdora 150010 template generator

Date: October 14, 2026. REA inspection: Chromium browser, 1440 × 1000 window, Spanish interface. Screenshots, the accessibility tree, DOM, and network requests were inspected. The local editor was not modified.

## Scope and access

The requested URL, containing `id=70847603`, displayed the “Log in to Pacdora” (“Iniciar sesión en Pacdora”) dialog in the isolated REA session. The following results therefore refer to the **public 150010 template**, opened without that identifier. Dimensions and contents of project 70847603 were not checked.

## Interface organization

The main pattern is a persistent canvas with a side panel whose contents change. Switching between Models and Basic leaves the dieline, 3D view, and export actions in place.

| Area | Observed behavior | Application to our generator |
|---|---|---|
| Header | Generator name, menu, save status, online design, share, and download | Keep the active model and download visible |
| Left navigation | Icon rail: Models, Basic, Advanced, and More | Use Models and Dimensions as primary entry points |
| Contextual panel | White container approximately 320 px wide, including an 80 px rail | Switch between library and form without leaving the editor |
| Central canvas | Dieline, dimension annotations, legend, and dimension summary on gray background | Reserve most space for the blank |
| Right column | 3D view with opening slider; formats and download explanation | Separate product view and export |
| Bottom toolbar | Selection, hand, zoom in/out, colors, and annotation visibility | Persistent controls for navigating the blank |

Screenshots: [Basic](basic_ready.png), [Models](models_loaded.png), [More](more_open.png), [Advanced](advanced_open.png).

## Model library

The library has Library and Projects tabs, search, and category selection. The observed category was Folding Boxes. Cards form two columns and display **the assembled box**, with small material swatches beneath. The list scrolls within the panel. A “Replace” (“Sustituir”) action was observed on items; replacement was not performed.

The implication for our interface is specific: the assembled-product thumbnail helps select a structure; the unfolded blank is used for editing afterward. Name and code should distinguish similar variants.

## Basic editor

The public template opened with these values:

| Parameter | Observed value |
|---|---|
| Length × width × height | 315 × 202 × 62 mm |
| Material | E-flute |
| Thickness | 1.5 mm; displayed range 1.1–2 mm |
| Manufacturing dimensions | 315 × 202 × 62 mm |
| Internal dimensions | 300 × 200 × 60 mm |
| External dimensions | 316 × 204.5 × 63 mm |

The mm/in selector was checked: 315 became 12.4016; 202 became 7.9528; 62 became 2.4409; and 1.5 became 0.0591. Returning to mm restored the initial values.

The material dropdown showed white paperboard, kraft paperboard, art paper, and corrugated board. No other material was selected, and its geometric allowance was not verified.

There are buttons for manufacturing, internal, and external dimensions. Clicking internal changed the control's active class and displayed a loading state; fields remained at 315/202/62 during the capture. **Conversion between modes remained unverified.** This session is insufficient to infer its formulas.

## Blank and tools

The legend distinguishes green bleed, blue cuts, and dashed red folds. The blank includes blue internal dimension annotations and overall exterior dimensions. The top summary displays all three dimension classes simultaneously.

The visibility menu offers overall dimensions, basic dimensions, cutting line, and annotation information. The color control opened a Cut editor with hexadecimal value `#2028b0`. Menu opening was checked; values were not changed.

The 3D view displays the assembled box and an opening slider. Its animation and synchronization with new dimensions were not tested. Dimension annotations on the blank do not themselves establish direct editability.

## Export and secondary features

AI, PDF, DXF, and 3D mockup options were displayed. Files were not downloaded, and availability for any particular account was not checked.

Advanced (“Anticipado”) displays numerous technical parameters and an invitation to upgrade to Business. Opening it adds many dimension annotations to the blank. This section can be omitted for the previously requested scope.

More (“Más”) groups services such as online design, printing, AI tools, and Illustrator integration. It is secondary to model selection, dimension editing, and obtaining the dieline.

## Inferred architecture

The DOM and requests suggest an application with shared state between library, parameters, and canvas. Requests for model details, categories, materials, and geometry were observed through routes such as `models/details`, `models/ctree`, `material_effect`, and `project/knife`. Their names and parameters show communication, not a complete specification of formulas.

During the library sequence, a `POST /api/v2/projects` appeared, followed by queries for a new identifier. This is not the requested project and does not establish lasting persistence. Event receipt order does not establish exact attribution of the request to a particular action.

## Priorities for our generator

1. Library with assembled-box thumbnails, name, and code; selection loads model parameters.
2. Dimensions panel with length, width, height, units, material, and thickness, limited to parameters actually supported by each generator.
3. Canvas updates with dimensions and preserves zoom and pan; clear dimension annotations and visibility controls.
4. Export linked to the current state. Add formats when a verified exporter exists for them.

Material allowances, internal/external modes, and 3D folding require implementation and validation per structure. This inspection does not allow them to be derived solely from the controls' appearance.

## Reproducible evidence

| File | REA evidence | Coverage |
|---|---|---|
| [Project](proyecto-evidencia.json) | `ev_6e1034e685c578f4c8bf2484e16f6cbb0edc8714066eba7913b9c5e318932172` | Exact URL; authentication required |
| [Basic](basico-evidencia.json) | `ev_ab4d82b6083ec032ea60501004c9482747bbad429dc016bfbca7b360696ac6e5` | Initial public state and capture |
| [Panels](paneles-evidencia.json) | `ev_11786905427e6c43b26c80a8d25f558ef541acd27ae098d1634876915997112c` | Library, mm/in, More, and Advanced |
| [Controls](controles-evidencia.json) | `ev_43446cea86be031c95fa044f36ecc7ad0c352bb8a5e81b7ea33a5f23dc7f432f` | Materials, internal mode, visibility, and color |

Limitations: captures are desktop-only; mobile responsiveness was not evaluated. The DOM retains hidden panels, so visibility was cross-checked against images. Some requests were still pending when captures ended; response bodies were not obtained, and formulas, downloading, and saving were not validated.
