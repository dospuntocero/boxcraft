[Español](analisis-pacdora.md) · English

# Pacdora analysis: storage boxes

Date: October 13, 2026. Inspection with REA and Chrome in a fresh unauthenticated session. Category: https://www.pacdora.com/es/dielines/storage-box-dielines

## Observed findings

- The category advertises 44 models. The capture's accessibility tree contains 15 product cards; this does not establish that all 44 are rendered simultaneously.
- It includes navigation by use/model, categories with counters, search, cards linked to detail pages, and explanatory content with FAQs.
- Structures vary: FEFCO 0201, 0202, 0203, and 0200; six-compartment, sliding, rigid, lidded, and handled boxes.
- The page combines SEO-oriented HTML (canonical, hreflang, JSON-LD, and metadata) with Vue resources and API v2 queries. Module names alone do not identify the entire implementation.
- The observed catalog request is GET /api/v2/models?pageSize=60&current=1&dielineNameKey=storage-box-dielines&mockup=false&offset=0&complexType=0. /models/ctree and /seo/info?id=180 are also queried.

## Inspected generator

Detail page: https://www.pacdora.com/es/dielines-detail/custom-dimensions-cartons-0201-dieline-200010

- Opens the template generator directly. The interface exposes length, width, height, mm/in selection, material, and thickness; it also distinguishes manufacturing, internal, and external dimensions.
- In this session the initial units were inches and the material was B-flute. Displayed manufacturing values were 17.0866 × 8.4252 × 10.9449 in, approximately 434 × 214 × 278 mm. Displayed thickness was 0.1181 in, approximately 3 mm. These initial values are not generalized to other sessions.
- The interface advertises AI, PDF, DXF, and a 3D mockup; it includes bleed, cut, and fold controls, sharing, and online design.
- Observed requests: GET /models/details?nameKey=custom-dimensions-cartons-0201-dieline-200010; /materials/science?pageSize=1000&scienceType=1; /models/preview?id=3; /project/knife?id=3&bleed=5&export_type=model; /modes/category/cal?cate_id=2&width=214&height=278&length=434.
- Permissions, plans, and Pro checks are also queried. Their presence does not establish which exports require payment.

## Interpretation

The experience separates discovery catalog and parametric generator. Calculation and dieline calls suggest server involvement; this capture does not establish where all geometry generation or 3D folding occurs. Distinguishing internal, external, and manufacturing dimensions means reproducing the interface is insufficient: material and thickness allowances must be understood.

For an independent implementation, the main components would be a family catalog, per-model parameter and limit schemas, cut and fold geometry, material allowances, blank view, 3D preview, and vector exporters. This is an architectural proposal, not recovered Pacdora source code.

## Evidence and limitations

- Category, DOM, accessibility, and network: ev_ee5a28cbdb2ae7ac302682e6cde12231fd4d8031d8fa14068a5787de5ed97544.
- FEFCO 0201 generator, DOM, accessibility, and network: ev_9d761dcb48852f2945c58238cd15c6fb302d95212ae0fead04916c8c4c2f29dc.
- Controlled execution evidence, not recovery of original source code. Identifiers refer to the REA session.
- The first pass changed no parameters and requested no export. The additional checks below extend that coverage. Response bodies were not captured; endpoints establish requests, not their contents or algorithms. All families, payment conditions, and mobile behavior were not verified.

## Additional verification: editing and downloading

Length was changed from 17.0866 to 20 inches and confirmed by removing focus from the field. The generator temporarily disabled fields, then updated the blank and dimensions:

| Dimension | Before (in) | After (in) |
| --- | --- | --- |
| Manufacturing length | 17.0866 | 20 |
| Internal length | 16.9291 | 19.8425 |
| External length | 17.1654 | 20.0787 |

Width, height, and thickness retained their initial values. The calculation request changed from length=434 to length=508, equivalent to 20 inches in millimeters. For these two samples, internal length is approximately 4 mm less than manufacturing length and external length is 2 mm greater. This describes the tested model and material, not a universal formula.

During interaction, POST and PUT /api/v2/projects, /projects/info and /project/knife queries with export_type=project, and /modes/category/info?project_id=…&type=project were observed. Editing can therefore create and update a server-side project even in this unauthenticated session; it is not purely local. Bodies were not inspected and persistence beyond the session was not confirmed.

Clicking “Download the dieline template” (“Descargar la plantilla de corte”) opened the login dialog with Google, Facebook, or email. Downloading required authentication in this test. No login occurred, no file was downloaded, and subsequent payment requirements were not determined.

Loading /scripts/wasm/knife2gltf/1.1.8/knife2gltf.min.wasm was also observed. Its name suggests client-side dieline-to-glTF conversion; loading the resource alone does not establish execution or its algorithm.

Full test evidence: ev_02ce3efdb55845f13649814802c778e459c1fe20ddca61f9bfbe75bfcf8444e2. All actions completed. The final state confirms the new dimensions and authentication dialog.

Bounded pending work: exported file and geometric accuracy, authenticated behavior and pricing, thickness/material variations, other families, and mobile.

## Received geometry and 3D conversion

The third pass captured response bodies, retained in evidencia-geometria.json. Readable response copies were extracted to geometria/knife.json, geometria/preview.json, and geometria/cal.json, along with the JavaScript bundle served to the browser. These are artifacts received from the site, not an independent implementation.

The /project/knife response contains actual geometry in layer.traditional: 13 faces, path commands (M, L, A, and Z), cutting lines, named folds, bleeds, transformations, and animation. Faces include position, width, height, and contour. This confirms that the server delivers a geometric representation of the dieline, beyond its parameters.

The inspected /modes/category/cal response returns thickness restrictions and layer metadata: minThickness=0.2 and maxThickness=9 for this query. It does not include blank contours. Observing that call during editing was therefore insufficient to attribute geometry generation to it. B-flute has its own limits of 2.5 to 3 mm in /project/knife; these are separate from category restrictions.

The original data distinguish size={L:430,W:210,H:270,D:3}, knifeSize={L:434,W:214,H:278}, and outSize={L:436,W:216,H:282}. They also include getKnifeSizeAdd and getOutSizeAdd. Values agree with the first test's interface dimensions; the full algebraic meaning of their coefficients is not established.

The pacdora-3d-CYhaKcyC1P.js bundle contains a function that initializes one of two WebAssembly wrappers, obtains _generateGLTFData, serializes the argument to JSON when needed, optionally allocates memory for bytes, and converts the result using UTF8ToString. This is static evidence of a local conversion route, not a runtime trace of that function. WebAssembly resource 1.1.8 was requested while loading the generator. Its internal implementation was not decompiled.

Current conclusion: the observed architecture is hybrid. The server provides dieline geometry and configuration; client JavaScript contains a route to a WebAssembly glTF generator. Exact execution of that route, all subsequent transformations, and AI/PDF/DXF exporters remain unverified.

Evidence: ev_77d8bd80d9fa88c43120d6cc5bd429c12c5968d9da9a0622cb273808367c498c. The MCP response exceeded the transport limit and was recovered by exporting the complete record without repeating the capture. These conclusions come from the specific responses and bundle fragments examined; they do not imply coverage of all JavaScript.

## Local capture view

geometria/vista-troquel.html and geometria/troquel-capturado.svg were generated with the reproducible geometria/generar-vista.py script. The view allows faces, names, cuts, and folds to be hidden; it retains received coordinates and does not recalculate the model. It includes a table of 6 folding stages and 12 rotations. All rotation references correspond to folds present in the capture.

Verification performed: valid SVG XML, 13 face contours, and 12 fold lines, matching the original JSON. Arcs were interpreted using SVG A commands and original fields; this interpretation still needs visual comparison with the editor. Bleed was not rendered because its alignment with the cut requires verification of transformations. This is not a manufacturing-validated blank.

Visual review in the integrated browser was blocked by its URL policy, which disallows file://. No attempt was made to bypass that restriction. Files are available locally; their appearance and browser control behavior were not checked.

## Static route of the 3D engine

The trace was extended in geometria/ruta-conversion-3d.md, with bundle locations. The flow selects and validates a layer, prepares geometry fields, chooses a converter by family, calls the WebAssembly wrapper, checks the result, and applies materials to exterior, interior, and edge meshes. CurveBox and SoftPacking have separate branches from the generic converter used by the Carton-compatible branch.

The original WebAssembly was extracted from the capture and its export table read without execution. The geometria/wasm-inventory.json inventory confirms generateGLTFData (function 1494), memory, malloc, and runtime utilities. The internal algorithm was not decompiled. This review describes static relationships; inferred calls are not presented as observed execution.

## Internal consistency and advanced parameters

geometria/validar-captura.py runs 8 checks and saves results in geometria/validacion-captura.json. All passed: unique names; connected graph of 13 faces and 12 folds (interpreting names as face pairs); contour references to folds; animation references; total fold length within 0.01 mm; cut endpoints inside 1340 × 494 mm; parameters within limits; and thickness compatible with the material. Under that interpretation, the graph is a tree.

The capture contains 6 additional parameters. Labels come from the server; their geometric effect was not tested by varying them:

| Code | Received description | Value | Range | Unit |
| --- | --- | --- | --- | --- |
| OF | High and Low | 2 | 0–3 | length |
| R | Chamfering | 3 | 1.5–6 | length |
| G | Length of paste | 45 | 10–212 | length |
| GT | Paste corner | 15 | 0–45 | angle |
| F | 摇盖长度 (flap length) | 108 | 15–214 | length |
| F1 | Side shaking cover | 110 | 10–110 | length |

This expands the schema required for reconstruction: beyond length, width, height, and thickness, the server provides glue-tab, corner, and flap parameters. Description-based correspondences are indicative; their formulas have not yet been recovered.

Validation does not establish correct assembly or suitability for manufacturing. It does not check intersections, production tolerances, arc interior extrema, total cut length, or folding collisions.

## Parametric experiments and first local generator

L=508 mm, W=254 mm, and H=304.8 mm were varied separately from 434 × 214 × 278 mm, restoring the base between changes. A thickness of 2.54 mm was also captured: it retains manufacturing dimensions, changes internal/external dimensions, and reduces R from 3 to 2.5. A general thickness-allowance formula was not inferred from only two samples.

With thickness fixed at 3 mm, an affine model per geometry field was built. It was checked against an independent combination: 457.2 × 228.6 × 279.4 mm. There were 822 numeric fields compared: faces, cuts, folds, and all other non-bleed fields match within 0.000001 units; 6 bleed coordinates differ by less than 0.0001 mm. Coefficients were not fitted using the check sample.

geometria/modelo-parametrico.py produces troquel-generado.svg and troquel-generado.json without querying Pacdora. It supports only the sample-bounded range and retains fixed material/thickness and advanced parameters. This is a limited empirical reconstruction, not recovery of the original algorithm or a guarantee of accuracy throughout that range. Usage, summarized formulas, and provenance are in geometria/README-modelo.md.

The advanced tab displays “Upgrade to unlock advanced parameters” and “Upgrade to Business” (“Actualiza para desbloquear parámetros avanzados” and “Actualizar a Negocios”). Values were observed, but manual changes remain pending because of that restriction; it was not bypassed.

Experiment and check captures ended with cleanup_incomplete and were recovered by export. All recorded actions completed and geometric responses used are present. This partial coverage allows comparison of retained data but does not establish complete process cleanup. IDs: ev_70c78216d8ca163ef7f939d0aed16da00ebc22365fb62afe71f36c34f435b46a and ev_e71c55c541c5bd0970f35ad5e7d9e8acfe58b97439dd0975c40c6f3260455e65. Advanced tab: ev_f5a6bc57aa5f99256bd933eac5f9a8ebfa1cfaf1ca8187ee3166b635309300bf.

## Second model: body lotion box 10001029

The user-specified page was analyzed and geometria/modelos/10001029/generar.py was built. This model belongs to the Pair family, with 13 faces, 76 cut commands, and 12 folds. The captured configuration is 60 × 45 × 120 mm and 350 g white paperboard, 0.5 mm thick.

This dieline automatically changes closures and flaps when basic dimensions vary. The first fit using only L,W,H was insufficient; samples were added to isolate those internal values without changing advanced controls. The final generator uses only the three basic parameters and retains material/thickness. It was checked against three states independent of training, with 784 numeric fields matching per state within 0.000001 units. Bleed and annotations are neither generated nor included in that comparison.

The supported interval is L=68.58–76.2, W=45–63.5, H=120–152.4 mm. The 60 × 45 × 120 troquel-base.svg is retained as a representation of the original capture. Usage, results, inferred formulas, and evidence are documented in geometria/modelos/10001029/README.md. Not validated for manufacturing, and the interval was not exhaustively checked.

## Third model: 102010, snap-lock bottom closure

geometria/modelos/102010/troquel-generado.svg was generated with the user-requested initial manufacturing dimensions: 120.6 × 60.6 × 161.1 mm, 350 g white paperboard, 0.5 mm thick. Geometry belongs to PairBuckle: 13 faces, 12 folds, and 80 cut commands, on a 377.9 × 282.25 mm blank. Default output preserves the included original geometry fields.

Samples showed a change in bottom structure: increasing L to 139.7 at W=60.6 raised cut-command count to 92; increasing W to 76.2 returned it to 80. A general linear L/W generator was therefore not published. The user confirmed continuing with the original dimensions, which remain fixed in the output.

An experimental H rule was retained, checked against 857 numeric fields at an L/W pair different from the fitting pair. Transfer to other heights of the base has no additional direct check. Bleed and annotations are excluded. Usage and limitations are in geometria/modelos/102010/README.md. Manufacturing and visual equivalence of arcs with the editor were not validated.

## Fourth model: 150010, flip-top mailer box

The link included project 70845997, which required authentication and did not provide its geometry. The user confirmed using the public template's initial manufacturing dimensions: 315 × 202 × 62 mm, 1.5 mm E-flute.

geometria/modelos/150010/troquel-base-publica.svg was generated: 19 faces, 22 folds, 89 outer-cut commands, and 4 interior slots, on a 576 × 590 mm blank. The shared renderer now includes holes paths, needed to represent those slots. XML, counts, and correspondence of included geometry with the capture were checked; the local view was rasterized and inspected.

The private project was not reconstructed, and no resizing engine was fitted for this model. Output retains the initial public dimensions chosen by the user. Bleed and annotations are excluded; manufacturing was not validated. Provenance and usage are in geometria/modelos/150010/README.md.

## Fifth model: 112047, gable box with cord and snap-lock bottom

geometria/modelos/112047/troquel-generado.svg was generated with initial dimensions 70 × 50 × 60 mm, 350 g white paperboard, 0.5 mm thick. The RoofWiringAndBottomBox family contains 19 faces, 18 folds, 72 outer-cut commands, and 4 top holes of radius 2 mm. The blank measures 252.5 × 152.5 mm.

The included geometric fields from the capture were retained, XML and counts were checked, and local output was rasterized and inspected. Total fold length agrees with the declared length within rounding to hundredths. No parametric variations were performed; the fixed initial configuration is delivered without bleed or annotations. Usage and evidence are in geometria/modelos/112047/README.md. Not validated for manufacturing.

## Sixth model: 12109002, cake box with handles

geometria/modelos/12109002/troquel-generado.svg was generated with initial dimensions 236 × 170 × 180 mm, 1.5 mm E-flute. The TrapezoidalFoldingAngleHandleTrayBox family contains 19 faces, 26 folds, 46 outer-cut commands, and 4 openings. The blank measures 824 × 1018 mm.

Included geometry fields were retained, XML and counts were checked, and fold length agrees with the declared value within rounding to hundredths. Local output was rasterized and inspected, including handles and side slots. The fixed initial configuration is delivered without bleed, annotations, or resizing. Usage and evidence are in geometria/modelos/12109002/README.md. Not validated for manufacturing.

## Seventh model: 112310, box with handle and snap-lock bottom

geometria/modelos/112310/troquel-generado.svg was generated with initial dimensions 302 × 152 × 182 mm, 1.5 mm E-flute. The BuckleSuitcaseForward family contains 16 faces, 15 folds, 72 outer-cut commands, and 3 openings. The blank measures 952 × 439 mm.

XML, counts, and preservation of included geometric fields were verified. Total fold length agrees with the declared value within rounding to hundredths. Local output was rasterized and inspected. The fixed initial configuration is delivered without bleed, annotations, or resizing. Usage and evidence are in geometria/modelos/112310/README.md. Not validated for manufacturing.

## Eighth model: 10001006, tuck-end box

geometria/modelos/10001006/troquel-generado.svg was generated with initial dimensions 40 × 40 × 130 mm, 350 g white paperboard, 0.5 mm thick. The Pair family contains 13 faces, 12 folds, and 76 outer-cut commands, with no interior openings. The blank measures 172.5 × 231 mm.

XML, counts, and preservation of included geometric fields were checked. Total fold length agrees with the declared value within rounding to hundredths. Local output was rasterized and inspected. Fixed initial configuration, without bleed, annotations, or resizing. Usage and evidence are in geometria/modelos/10001006/README.md. Not validated for manufacturing.

## Ninth model: 10002003, double hanging-tab box

geometria/modelos/10002003/troquel-generado.svg was generated with initial dimensions 100 × 40 × 120 mm, 350 g white paperboard, 0.5 mm thick. The PairWithHook family contains 16 faces, 15 folds, 94 outer-cut commands, and 2 hanging openings. The blank measures 295.5 × 263.75 mm.

XML, counts, and preservation of included geometric fields were checked. Total fold length agrees with the declared value within rounding to hundredths. Local output was rasterized and inspected, including the two hanging openings. Fixed initial configuration, without bleed, annotations, or resizing. Usage and evidence are in geometria/modelos/10002003/README.md. Not validated for manufacturing.

## Tenth model: 180370, French fries carton

geometria/modelos/180370/troquel-generado.svg was generated with initial dimensions 120 × 80 × 160 mm, 250 g white paperboard, 0.35 mm thick. The ChipBox family contains 10 faces, 9 folds, and 26 outer-cut commands, with no interior openings. The blank measures 314.301396 × 453 mm.

XML, counts, and preservation of included geometric fields were checked. Total fold length agrees with the declared value within rounding to hundredths. Local output was rasterized and inspected, including curved contours. Fixed initial configuration, without bleed, annotations, or resizing. Usage and evidence are in geometria/modelos/180370/README.md. Not validated for manufacturing.

## Eleventh model: 180320, sandwich box with window

geometria/modelos/180320/troquel-generado.svg was generated with initial dimensions 120 × 75 mm, 350 g white paperboard, 0.5 mm thick. These are the two exposed initial dimensions; H=0 is an auxiliary API field and is not presented as physical height. The WindowLockSandwichBox family contains 12 faces, 13 folds, 63 outer-cut commands, and one window. The blank measures approximately 289.4533 × 289.3779 mm.

XML, counts, and preservation of included geometric fields were checked. Total fold length agrees with the declared value within rounding to hundredths. Local output was rasterized and inspected. Fixed initial configuration, without bleed, annotations, or resizing. Usage and evidence are in geometria/modelos/180320/README.md. Not validated for manufacturing.
