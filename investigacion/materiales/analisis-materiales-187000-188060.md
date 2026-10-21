# Análisis de materiales · 187000 y 188060

Fecha: 2026-10-20 · Ámbito: solo lectura sobre la interfaz pública de Pacdora, sin cuenta ni descarga de archivos.

Fuentes: páginas públicas del editor (`dielines-detail`), catálogo local `editor-troqueles/dist/assets/materiales.json`, capacidades locales `editor-troqueles/dist/assets/capacidades-materiales.json` y geometrías base de `geometria/modelos/187000/` y `geometria/modelos/188060/`.

Capturas y DOM de esta revisión: [`capturas-187000-188060/manifest.json`](capturas-187000-188060/manifest.json). Cada archivo conserva su SHA-256 y la referencia REA de la observación.

## 1. Estado local actual

| Modelo | Material | Espesor | Perfiles adicionales | `onlyManufacturing` | Motivo registrado |
|---|---|---|---:|---|---|
| 187000 | Cartón blanco 350 g (103) + 210 g (100) + kraft 190 g (108) | 0,5 / 0,27 / 0,26 mm | 2 | Sí | Verificados 350 g, 210 g y 190 g; faltan capturas para el resto |
| 188060 | Cartón blanco 350 g (103) | 0,5 mm | 0 | Sí | Solo material y espesor originales; motor experimental |

187000 expone ya tres materiales; 188060 sigue con uno. El resto del catálogo no se ofrece porque no hay geometría capturada para esas combinaciones.

## 2. Menú real de Pacdora

Captura del selector completo, grupo por grupo, el 2026-10-20. Evidencias:
`ev_a6f225bbd4ae22fc89c7b570f40486177f168c65748853812cf09fbe32a3cb01` (187000) y
`ev_f69dd90b62fe4f5034dc2cddb0ee8dceb321aa999d83056d2ecb49214002999a` (188060).

### 187000 · Caja almohada

| Grupo | Material | Espesor | Estado | ID local |
|---|---|---:|---|---:|
| Cartulina blanca | Cartón blanco 210 g (0,27 mm) | 0,27 | Disponible | 100 |
| Cartulina blanca | Cartón blanco 250 g (0,35 mm) | 0,35 | Disponible | 101 |
| Cartulina blanca | Cartón blanco 300 g (0,42 mm) | 0,42 | Disponible | 102 |
| Cartulina blanca | Cartón blanco 350 g (0,5 mm) | 0,50 | Activo (original) | 103 |
| Cartulina blanca | Cartón blanco personalizado | 0,1–0,8 | Disponible | 8 |
| Cartulina blanca | Cartón blanco 400 g (0,55 mm) | 0,55 | Deshabilitado | 104 |
| Cartulina kraft | Cartón kraft 120 g (0,14 mm) | 0,14 | Deshabilitado | 107 |
| Cartulina kraft | Cartón kraft 190 g (0,26 mm) | 0,26 | Disponible | 108 |
| Cartulina kraft | Cartón kraft 250 g (0,33 mm) | 0,33 | Disponible | 109 |
| Cartulina kraft | Cartón kraft 350 g (0,46 mm) | 0,46 | Disponible | 110 |
| Cartulina kraft | Cartón kraft personalizado | 0,1–0,8 | Disponible | 7 |
| Papel arte | Papel estucado 200 g (0,2 mm) | 0,20 | Disponible | 47 |
| Papel arte | Papel estucado 350 g (0,32 mm) | 0,32 | Disponible | 42 |
| Papel arte | Papel estucado personalizado | 0,1–0,5 | Disponible | 153 |
| Cartón corrugado | Todos (personalizado, Onda N, F, E, B, C, BE, A, BB, BC, AB, AC, AA, BCB, BAC, BAA, ACA, AAA) | — | Deshabilitados | — |

Resultado: **12 combinaciones habilitadas** (incluidos los tres personalizados). El rango de espesor que acepta el modelo en el menú es **0,20–0,50 mm**; 0,14 y 0,55 quedan deshabilitados. No se ofrece cartón corrugado.

### 188060 · Caja hexagonal

| Grupo | Material | Espesor | Estado | ID local |
|---|---|---:|---|---:|
| Cartulina blanca | Cartón blanco 210 g (0,27 mm) | 0,27 | Disponible | 100 |
| Cartulina blanca | Cartón blanco 250 g (0,35 mm) | 0,35 | Disponible | 101 |
| Cartulina blanca | Cartón blanco 300 g (0,42 mm) | 0,42 | Disponible | 102 |
| Cartulina blanca | Cartón blanco 350 g (0,5 mm) | 0,50 | Activo (original) | 103 |
| Cartulina blanca | Cartón blanco 400 g (0,55 mm) | 0,55 | Disponible | 104 |
| Cartulina blanca | Cartón blanco personalizado | 0,1–0,8 | Disponible | 8 |
| Cartulina kraft | Cartón kraft 120 g (0,14 mm) | 0,14 | Deshabilitado | 107 |
| Cartulina kraft | Cartón kraft 190 g (0,26 mm) | 0,26 | Disponible | 108 |
| Cartulina kraft | Cartón kraft 250 g (0,33 mm) | 0,33 | Disponible | 109 |
| Cartulina kraft | Cartón kraft 350 g (0,46 mm) | 0,46 | Disponible | 110 |
| Cartulina kraft | Cartón kraft personalizado | 0,1–0,8 | Disponible | 7 |
| Papel arte | Papel estucado 200 g (0,2 mm) | 0,20 | Disponible | 47 |
| Papel arte | Papel estucado 350 g (0,32 mm) | 0,32 | Disponible | 42 |
| Papel arte | Papel estucado personalizado | 0,1–0,5 | Disponible | 153 |
| Cartón corrugado | Onda N | 0,8–1,0 | Disponible | 10 |
| Cartón corrugado | Onda F | 1,0–1,2 | Disponible | 6 |
| Cartón corrugado | Onda E | 1,1–2,0 | Disponible | 5 |
| Cartón corrugado | Cartón corrugado personalizado | 0,8–15 | Disponible | 152 |
| Cartón corrugado | Onda B y superiores (C, BE, A, BB, BC, AB, AC, AA, BCB, BAC, BAA, ACA, AAA) | ≥ 3 | Deshabilitados | — |

Resultado: **17 combinaciones habilitadas**. Rango de espesor aceptado en el menú: **0,20–2,00 mm**. A diferencia de 187000, aquí sí se ofrece corrugado (Onda N, F y E) y el cartón blanco de 400 g.

## 3. Comprobaciones de geometría

### 187000: la geometría de corte no cambia con el material (en lo comprobado)

Se cambió el material en el editor y se comparó el trazado de corte completo contra la geometría base de 350 g / 0,5 mm.

| Configuración | Espesor | Trazado de corte | Diferencia máxima | Evidencia |
|---|---:|---|---:|---|
| Cartón blanco 210 g | 0,27 | Idéntico (76 valores numéricos) | 0,000 mm | `ev_e47c1be1a068592c16db62f1f7eafa053c00fdfe935c2bb5fae670c16e9ea5a3` |
| Cartón kraft 190 g | 0,26 | Idéntico (76 valores numéricos) | 0,000 mm | `ev_9f9f9c5433ef27591d4e864e7930435bd9757cb6124dfb6e3cc52c45251d99bb` |

En ambas selecciones el editor mantiene 118 × 70 × 25 mm de manufactura, fija el espesor (control deshabilitado en 0,27 y 0,26) y deja solo el modo manufactura. El dibujo y las cotas no cambian.

Conclusión acotada: para 187000 el corte parece depender solo de L/W/H, no del material ni del espesor. Los dos materiales alternativos comprobados pueden reutilizar la capa base sin pérdida geométrica. No se comprobaron los otros nueve materiales del menú.

### 188060: la geometría sí cambia con el material

Se seleccionó Onda E (1,5 mm). El editor pasó a «Espesor a la medida» con rango **1,1–2 mm**, habilitó los tres modos y recalculó interiores/exteriores:

| Medida | 350 g / 0,5 mm | Onda E / 1,5 mm |
|---|---|---|
| Manufactura | 100,6 × 40,6 × 181,6 | 100,6 × 40,6 × 181,6 |
| Interior | 100 × 40 × 180 | 98,6 × 38,6 × 176,6 |
| Exterior | 145,2 × 41 × 222,6 | 145,8 × 41,6 × 223,2 |
| Plano | 336,7 × 262,8 | 336,2 × 262,8 |

El contorno de corte conserva los 28 comandos y la topología, pero **10 vértices cambian**: el ancho exterior baja 0,5 mm (336,7 → 336,2) y los vértices de sangría/interior se desplazan hasta 3,0 mm (por ejemplo, 15 → 13 y 241 → 238). Evidencia: `ev_85a4da4fd67f92017e9649d0248bf12ba7c46f4b578bb2b47e4887f03bf62245`.

Conclusión: en 188060 no se puede reutilizar la capa base para otro material. Cada combinación necesita su propia captura de geometría y sus compensaciones interior/exterior.

## 4. Brechas frente a la capacidad local

| Aspecto | 187000 | 188060 |
|---|---|---|
| Materiales ofrecidos por Pacdora | 12 | 17 |
| Materiales configurados localmente | 3 (103, 100, 108) | 1 |
| Rango de espesor del menú | 0,20–0,50 | 0,20–2,00 |
| `observedThicknessLimits` local | [0,20; 0,50] | [0,5; 0,5] |
| `onlyManufacturing` local | Correcto (la interfaz solo muestra manufactura) | **Contradicho**: Pacdora muestra interiores y exteriores (`IsOnlyManufacture = 0` en `base/knife-00.json`) |
| Dependencia geométrica del material | No observada en 2 de 12 materiales | Sí, confirmada en Onda E |
| Compensaciones interior/exterior | No aplican (solo manufactura) | Cambian con el material; no capturadas localmente |

Riesgo principal: habilitar materiales por coincidencia de espesor del catálogo. En 188060 el corte cambia aunque el espesor sea parecido; en 187000 la coincidencia se verificó, pero solo para dos materiales.

## 5. Qué se habilitó ya

### 187000

Se añadieron dos perfiles exactos que reutilizan la capa base, mediante [`incorporar-materiales-187000.py`](../../editor-troqueles/incorporar-materiales-187000.py):

| Material | ID | Espesor | Capa | Offsets | Límites |
|---|---:|---:|---|---|---|
| Cartón blanco 210 g | 100 | 0,27 | Base 187000 | 0 / 0 / 0 | Medidas fijas |
| Cartón kraft 190 g | 108 | 0,26 | Base 187000 | 0 / 0 / 0 | Medidas fijas |

Los perfiles quedaron con `geometryStatus: "verified"`, `onlyManufacturing: true` y la evidencia de la comparación. `observedThicknessLimits` se amplió a [0,20; 0,50] y la interfaz muestra 103, 100 y 108. Los otros nueve materiales del menú (blanco 250/300/personalizado, kraft 250/350/personalizado, arte 200/350/personalizado) requieren una comprobación equivalente antes de habilitarse.

Pruebas: `materials.test.cjs` cubre la reutilización exacta de la capa, el rechazo de medidas fuera del rango fijo y el rechazo de un espesor no configurado.

### 188060

Nada adicional al material original con la evidencia actual. Onda E ya demostró que el trazado cambia; habilitarla reutilizando la capa base introduciría un error de hasta 3 mm. Se necesita la respuesta de geometría de cada material.

## 6. Plan de captura recomendado

Los 22 escenarios ya están preparados, uno por material y espesor, en [`capturas-escenarios/index.json`](capturas-escenarios/index.json); las instrucciones y el colector están en [`README-capturas-187000-188060.md`](README-capturas-187000-188060.md). Secuencia:

1. Para cada material habilitado, capturar la respuesta `project/knife` con las medidas de manufactura fijas (118 × 70 × 25 en 187000; 100,6 × 40,6 × 181,6 en 188060).
2. Verificar la selección efectiva en `layer.traditional.science_id` y `layer.traditional.thickness`, no solo en el control visible.
3. Guardar corte, pliegues, caras, aberturas, `knifeSize`, `size`, `outSize` y compensaciones.
4. Comparar cada respuesta contra la base y decidir: capa exacta reutilizable (caso 187000) o capa propia por material (caso 188060).
5. En 188060, capturar además los extremos del intervalo de espesor de cada corrugado (Onda E: 1,1 y 2,0 mm; Onda F: 1,0 y 1,2; Onda N: 0,8 y 1,0) antes de habilitar el control continuo.
6. Añadir cada perfil a `capacidades-materiales.json` solo después de la comparación y ampliar `materials.test.cjs` con los casos nuevos; 187000 ya tiene el primer par incorporado.

Prioridad sugerida: 187000 (blanco 250/300/personalizado, kraft 250/350/personalizado, arte 200/350/personalizado) y 188060 (Onda E, Onda N, Onda F, blanco 400 g y luego el resto).

## 7. Limitaciones

- Las comprobaciones son observaciones del DOM renderizado, no de la respuesta `project/knife`; la identidad exacta de `science_id` y las compensaciones de API quedan pendientes.
- No se validó armado físico, tolerancias de fabricación ni exportación AI/PDF/DXF.
- Solo se comprobaron dos materiales alternativos en 187000 y uno en 188060; el resto del menú está observado pero no verificado geométricamente.
- Al cambiar de material, el editor abrió una sesión de diseño anónima (`?id=...`); no se usó cuenta ni se descargaron archivos.
- El menú puede variar con las medidas, el espesor o la fecha; las listas corresponden a las medidas iniciales indicadas.
