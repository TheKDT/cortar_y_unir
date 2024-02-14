**Descripción del uso principal:**
Este código proporciona una interfaz de usuario (GUI) para dos funcionalidades principales: cortar y unir imágenes. Con la opción de "Cortar", el usuario puede seleccionar una carpeta que contiene imágenes y especificar en cuántas partes desea dividirlas. Las imágenes cortadas se guardarán en una subcarpeta dentro de la carpeta original. Con la opción de "Unir", el usuario puede seleccionar una carpeta que contiene imágenes ya divididas y estas se combinarán en una sola imagen verticalmente, guardándose en la misma carpeta.

**Descripción detallada de cómo usarlo y los factores a tener en cuenta:**

**► Cortar imágenes:**
- Al hacer clic en el botón "Cortar", se abrirá un diálogo para que el usuario seleccione una carpeta que contiene las imágenes que desea cortar.
- Después de seleccionar la carpeta, se solicitará al usuario que ingrese el número de partes en las que desea dividir las imágenes.
- Es importante tener en cuenta que el número de partes debe ser un número entero entre 1 y 100.
- Una vez que se completa el proceso de corte, las imágenes cortadas se guardarán en una subcarpeta llamada "Corte" dentro de la carpeta original.
- Se mostrará un mensaje de éxito informando al usuario que las imágenes han sido cortadas correctamente.

**► Unir imágenes:**
- Al hacer clic en el botón "Unir", se abrirá un diálogo para que el usuario seleccione una carpeta que contiene las imágenes que desea unir.
- Las imágenes seleccionadas serán combinadas en una sola imagen verticalmente.
- La imagen combinada se guardará en la misma carpeta donde se encuentran las imágenes originales.
- Se mostrará un mensaje de éxito informando al usuario que las imágenes han sido unidas y guardadas correctamente.

**Consideraciones adicionales:**
- Las imágenes deben estar en formato PNG, JPG o JPEG para poder ser procesadas correctamente.
- Se recomienda tener cuidado al seleccionar las carpetas y al ingresar el número de partes durante el proceso de corte para evitar errores o resultados inesperados.
- Es importante tener en cuenta que el proceso de unión de imágenes puede consumir una cantidad considerable de recursos, especialmente si las imágenes son de gran tamaño o hay muchas de ellas.
