# KEXNARV.github.io

Herramientas para realizar un ANOVA en Python.

## Scripts

- `run_analysis.py`: contiene utilidades para formatear los resultados. Incluye `format_text` para un reporte en texto y `generate_html` para crear una página web con las tablas.
- `anova.py`: reúne las funciones estadísticas. Se añadió `tabla_shapiro` para obtener las diferencias pareadas utilizadas por la prueba de Shapiro-Wilk.
- `gui.py`: interfaz gráfica en Tkinter que permite ingresar los valores en una cuadrícula y añadir o eliminar filas y columnas. Los resultados se muestran en una ventana emergente.

## Uso

```bash
python gui.py
```

Al ejecutar la aplicación se abrirá la interfaz gráfica. Tras introducir los datos y pulsar **Mostrar resultados** se abrirá una ventana con el reporte en texto.

La función `generate_html` produce además un archivo con todas las tablas, incluida una nueva sección que muestra las diferencias pareadas y sus pesos utilizadas por la prueba de Shapiro-Wilk.

Para generar el archivo HTML es necesario contar con la biblioteca **SciPy** instalada:

```bash
pip install scipy
python run_analysis.py
```
