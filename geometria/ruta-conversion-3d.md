# Ruta estática del troquel al modelo 3D

Fuente: pacdora-3d-CYhaKcyC1P.js, capturado en la evidencia ev_77d8bd80d9fa88c43120d6cc5bd429c12c5968d9da9a0622cb273808367c498c. Los nombres minificados solo identifican este bundle.

1. `uV` selecciona la primera capa que no sea gris y tenga datos en `layer`. `dV` obtiene la lista de capas desde `modeCate.layerList` o, como alternativa, las claves disponibles en `layer`.
2. `mV` comprueba caras y sus contornos, cortes, pliegues, sangrías, tamaño total y espesor. `hV` lanza un error con los campos faltantes si la validación falla.
3. `gV` copia los campos de la capa seleccionada al nivel superior del objeto de entrada. Contempla las dos variantes de nombre `holes` y `holds`.
4. `bV` elige un conversor según `modeCate.code`: `CurveBox` usa `CB`, `SoftPacking` usa `wB` y las otras rutas usan `XS`. En la respuesta FEFCO 0201 el código observado es `Carton`, compatible con esta última rama. No se ejecutó aquí esa llamada.
5. `XS` inicializa un wrapper de WebAssembly: `ali` para zh-CN, `aws` para los demás idiomas. Serializa el objeto, usa `allocateUTF8`, llama a `_generateGLTFData` y decodifica el resultado con `UTF8ToString`. La llamada desde `bV` pasa los argumentos auxiliares `0, null, 0, false`.
6. `vV` y `yV` revisan el resultado cuando es una cadena que comienza con `{`: comprueban escena, nodos y mallas, y lanzan un error si el JSON está mal formado o el modelo está vacío. Esta rama no verifica toda la especificación glTF.
7. `bV` pasa el resultado a `nD` y asigna la cadena a `window.gltfData`.
8. En la inicialización de la clase `xV`, el objeto devuelto se busca por nombres como `traditional_outer`, `traditional_inner` y `traditional_side`. Se aplican materiales distintos a exterior, interior y cantos. En modelos que no son CurveBox ni SoftPacking, se invierte la componente V de las coordenadas UV de ciertas mallas.

Ubicaciones de referencia: `uV` comienza en el desplazamiento 1862741, `gV` en 1864278, `bV` en 1865852 y su llamada a `XS` aparece en 1866081. Son índices de caracteres del texto decodificado en Python, base cero; no direcciones de memoria ni líneas del código original.

## Inventario WebAssembly

Se extrajo el binario de los bytes ya capturados, sin descargarlo de nuevo ni ejecutarlo. Tamaño: 1.206.159 bytes. SHA-256: a5fa190dd24abea89f6eeadbeadfb69520647b66410403e687662837d2ba01b4.

La tabla de exportaciones contiene `generateGLTFData` con índice de función 1494, `malloc`, funciones de pila, memoria y utilidades de runtime. El inventario completo está en wasm-inventory.json. Estos símbolos corroboran la interfaz usada por el wrapper; no demuestran el algoritmo interno ni la fidelidad del modelo generado.

## Límites

Es una traza estática manual de fragmentos del JavaScript recibido, respaldada por la captura de la carga del WASM. No es una observación de cada llamada en ejecución, una decompilación del WASM ni una reproducción del motor. No se ejecutó código descargado durante esta revisión offline. Quedan pendientes el formato exacto de salida, la gestión de recursos del motor y los exportadores de impresión.
