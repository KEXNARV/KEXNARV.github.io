# KEXNARV.github.io

Herramientas para realizar un ANOVA en Python.

## Scripts

- `run_analysis.py`: contiene utilidades para formatear los resultados. Incluye `format_text` para un reporte en texto y `generate_html` para crear una página web con las tablas.
- `gui.py`: interfaz gráfica en Tkinter que permite ingresar los valores en una cuadrícula y añadir o eliminar filas y columnas. Los resultados se muestran en una ventana emergente.
- Los reportes incluyen la tabla completa de la prueba de normalidad de Shapiro-Wilk con el tamaño de la muestra, el estadístico W y el valor p.

## Uso

```bash
python gui.py
```

Al ejecutar la aplicación se abrirá la interfaz gráfica. Tras introducir los datos y pulsar **Mostrar resultados** se abrirá una ventana con el reporte en texto.
