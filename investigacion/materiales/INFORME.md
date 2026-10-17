# Revisión REA de materiales — 16 de octubre de 2026

Estado: parcial; cambios locales, sin publicar. Se conservan los materiales originales de las once cajas y se habilitan 64 configuraciones adicionales medidas en diez cajas.

Observaciones: las respuestas contienen la geometría resultante y la compensación interior/exterior. El campo science conserva el material original en ciertas respuestas; la selección efectiva se obtiene de layer.traditional.science_id y layer.traditional.thickness. Cambiar dimensiones puede sustituir automáticamente el material o ajustar parámetros avanzados, de modo que no es válido atribuir el trazado a la selección solicitada sin comprobar el resultado.

Limitaciones: las capturas con cierre incompleto se conservaron como observaciones parciales. Se usan únicamente respuestas completas de geometría capturadas; no se afirma que la sesión haya cerrado correctamente. La fuente devolvió 403 en /projects y /modes/category/cal; los controles quedaron deshabilitados y las capturas posteriores no aportaron variaciones válidas. No se eludió esa restricción.

Resultados no habilitados: el ajuste afín por dimensiones y el ajuste continuo por espesor no superaron la validación; hay cambios de topología, redondeos y parámetros adicionales. Las configuraciones nuevas se limitan a medidas exactas capturadas. No se generaliza compatibilidad por igualdad de espesor ni por solapamiento de rangos del catálogo.

Cobertura y cadena de evidencia: collected.json enlaza cada archivo de respuesta con la captura y su referencia; observed-profile-ledger.json enumera los casos habilitados. Los archivos *-result.json y retained-audit-final.json contienen las capturas completas o parciales de REA. profile-build-report.json y physical-fit-findings.md documentan los ajustes rechazados.

Validación: 56 pruebas Node aprobadas; 75 combinaciones habilitadas recorridas mediante la interfaz, sin mensajes de error, sin planos vacíos y con la descarga habilitada. La comprobación automatizada de descarga por el evento del navegador no concluyó; no se declara verificación del archivo descargado.

Pendiente: completar alternativas de 12109002, completar la matriz de otros materiales/espesores por caja y reconstruir el comportamiento de dimensiones variables para los nuevos materiales sin extrapolar muestras.
