# Matriz de cobertura 15030101

Configuración de manufactura: 150 × 150 × 50 mm. Opciones disponibles comprobadas en el selector y mediante respuestas de geometría. Espesores personalizados: muestras discretas; no intervalo continuo habilitado.

| Material | ID | Espesores comprobados (mm) | Estado |
|---|---:|---|---|
| Cartón blanco 350g (0,5mm) | 103 | 0.5 | Geometrías completas e integración local |
| Cartón blanco 210g (0,27mm) | 100 | 0.27 | Geometrías completas e integración local |
| Cartón blanco 250g (0,35mm) | 101 | 0.35 | Geometrías completas e integración local |
| Cartón blanco 300g (0,42mm) | 102 | 0.42 | Geometrías completas e integración local |
| Cartón blanco personalizado | 8 | 0.2, 0.35, 0.5 | Geometrías completas e integración local |
| Cartón kraft 190g (0,26mm) | 108 | 0.26 | Geometrías completas e integración local |
| Cartón kraft 250g (0,33mm) | 109 | 0.33 | Geometrías completas e integración local |
| Cartón kraft 350g (0,46mm) | 110 | 0.46 | Geometrías completas e integración local |
| Cartón kraft personalizado | 7 | 0.2, 0.35, 0.5 | Geometrías completas e integración local |
| Papel estucado 200g (0,2mm) | 47 | 0.2 | Geometrías completas e integración local |
| Papel estucado 350g (0,32mm) | 42 | 0.32 | Geometrías completas e integración local |
| Papel estucado personalizado | 153 | 0.2, 0.35, 0.5 | Geometrías completas e integración local |

Opciones deshabilitadas en estas medidas: cartón blanco 400g (0,55 mm), kraft 120g (0,14 mm) y todos los corrugados listados por el selector. Esto no acredita incompatibilidad física fuera de esta configuración.

Los personalizados se comprobaron en 0,2 / 0,35 / 0,5 mm. El catálogo puede declarar rangos más amplios, pero la respuesta de límites de esta caja y medidas devuelve 0,2–0,5 mm. El paso de edición no se estableció.

## Configuraciones de otras dimensiones

Material original ID 103, 0,5 mm; disponibles como casos exactos mediante el generador CLI:

- 160 × 150 × 50 mm — `parametricas/knife-02.json`.
- 150 × 160 × 50 mm — `parametricas/knife-04.json`.
- 150 × 150 × 60 mm — `parametricas/knife-06.json`.
- 155 × 150 × 60 mm — `parametricas/knife-07.json`.
- 155 × 155 × 60 mm — `parametricas/knife-08.json`.
- 155 × 150 × 50 mm — `independiente/knife-02.json`.
- 155 × 155 × 50 mm — `independiente/knife-03.json`.
- 155 × 155 × 55 mm — `independiente/knife-04.json`.

No se ofrece interpolación de medidas ni espesores. El ajuste dimensional afín falló y permanece deshabilitado; ver `validacion-parametrizacion.json`.
