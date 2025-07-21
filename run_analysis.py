from anova import (
    run_anova,
    calculos_por_tratamiento,
    calcular_lsd,
    calcular_tukey,
    calcular_duncan,
    prueba_shapiro,
    prueba_bartlett,
)


def generate_html(groups):
    anova_res = run_anova(groups)
    calcs = calculos_por_tratamiento(groups)
    lsd = calcular_lsd(groups)
    tukey = calcular_tukey(groups)
    duncan = calcular_duncan(groups)
    shapiro = prueba_shapiro(groups)
    bartlett = prueba_bartlett(groups)

    html = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "    <meta charset='UTF-8'>",
        "    <title>Resultados ANOVA</title>",
        "    <style>table{border-collapse:collapse}td,th{border:1px solid #ccc;padding:4px;text-align:center}</style>",
        "</head>",
        "<body>",
        "<h1>Resultados ANOVA</h1>",
    ]

    html.append("<h2>Promedios</h2>")
    html.append("<table><thead><tr><th>Grupo</th><th>Media</th></tr></thead><tbody>")
    for g, m in anova_res['group_means'].items():
        html.append(f"<tr><td>{g}</td><td>{m:.4f}</td></tr>")
    html.append("</tbody></table>")

    html.append("<h2>Estadísticas globales</h2>")
    html.append(
        "<table><thead><tr><th>Y..</th><th>N</th><th>Ȳ..</th><th>Suma de cuadrados total</th></tr></thead>"
    )
    html.append(
        f"<tbody><tr><td>{calcs['total_general']}</td><td>{calcs['N']}</td><td>{calcs['media_global']:.4f}</td><td>{calcs['suma_cuadrados_total']:.4f}</td></tr></tbody></table>"
    )

    html.append("<h2>Estadísticas por tratamiento</h2>")
    html.append(
        "<table><thead><tr><th>Tratamiento</th><th>Yi·</th><th>ni</th><th>Ȳi</th><th>τ̂i</th></tr></thead><tbody>"
    )
    for g in calcs['totales_por_tratamiento'].keys():
        html.append(
            f"<tr><td>{g}</td><td>{calcs['totales_por_tratamiento'][g]}</td><td>{calcs['n_por_tratamiento'][g]}</td><td>{calcs['medias_por_tratamiento'][g]:.4f}</td><td>{calcs['desviaciones_respecto_media_global'][g]:.4f}</td></tr>"
        )
    html.append("</tbody></table>")

    html.append("<h2>Tabla ANOVA</h2>")
    html.append(
        "<table><thead><tr><th>FV</th><th>SC</th><th>GL</th><th>CM</th><th>F0</th><th>Valor-p</th></tr></thead><tbody>"
    )
    html.append(
        f"<tr><td>Tratamientos</td><td>{anova_res['SC_TRAT']:.4f}</td><td>{anova_res['GL_TRAT']}</td><td>{anova_res['CM_TRAT']:.4f}</td><td>{anova_res['F0']:.4f}</td><td>{anova_res['p_value']:.4f}</td></tr>"
    )
    html.append(
        f"<tr><td>Error</td><td>{anova_res['SC_E']:.4f}</td><td>{anova_res['GL_E']}</td><td>{anova_res['CM_E']:.4f}</td><td></td><td></td></tr>"
    )
    html.append(
        f"<tr><td>Total</td><td>{anova_res['SC_T']:.4f}</td><td>{anova_res['GL_T']}</td><td></td><td></td><td></td></tr>"
    )
    html.append("</tbody></table>")

    html.append("<h2>Prueba de normalidad (Shapiro-Wilk)</h2>")
    html.append(
        "<table><thead><tr><th>N</th><th>W</th><th>Valor-p</th></tr></thead>"
        f"<tbody><tr><td>{shapiro['n']}</td><td>{shapiro['w']:.4f}</td><td>{shapiro['p_value']:.4f}</td></tr></tbody></table>"
    )
    html.append(
        "<table><thead><tr><th>i</th><th>a<sub>i</sub></th><th>X(n-i+1)-X(i)</th><th>a<sub>i</sub>(X(n-i+1)-X(i))</th></tr></thead><tbody>"
    )
    for fila in shapiro['tabla']:
        html.append(
            f"<tr><td>{fila['i']}</td><td>{fila['ai']:.4f}</td><td>{fila['diff']:.4f}</td><td>{fila['ai_diff']:.4f}</td></tr>"
        )
    html.append("</tbody></table>")

    html.append("<h2>Prueba de homogeneidad (Bartlett)</h2>")
    html.append(
        "<table><thead><tr><th>k</th><th>Chi-cuadrado</th><th>Valor-p</th></tr></thead>"
        f"<tbody><tr><td>{bartlett['k']}</td><td>{bartlett['chi2']:.4f}</td><td>{bartlett['p_value']:.4f}</td></tr></tbody></table>"
    )
    html.append(
        "<table><thead><tr><th>Grupo</th><th>n<sub>i</sub></th><th>Varianza</th></tr></thead><tbody>"
    )
    for fila in bartlett['tabla']:
        html.append(
            f"<tr><td>{fila['grupo']}</td><td>{fila['n']}</td><td>{fila['var']:.4f}</td></tr>"
        )
    html.append("</tbody></table>")

    def comparisons_table(title, res, label):
        html.append(f"<h2>{title}</h2>")
        html.append(
            f"<table><thead><tr><th>Comparación</th><th>|Ȳi - Ȳj|</th><th>SE</th><th>{label}</th><th>Diferencia</th><th>Significativo</th></tr></thead><tbody>"
        )
        for key, comp in res['comparaciones'].items():
            val_label = 'lsd' if label == 't crítico' else ('hsd' if label == 'q crítico' else 'dms')
            diff_val = comp.get(val_label, 0)
            crit = comp.get('t_crit') or comp.get('q_crit')
            html.append(
                f"<tr><td>{comp['grupo1']} - {comp['grupo2']}</td><td>{comp['diff']:.4f}</td><td>{comp['se']:.4f}</td><td>{crit:.4f}</td><td>{diff_val:.4f}</td><td>{'Sí' if comp['significant'] else 'No'}</td></tr>"
            )
        html.append("</tbody></table>")

    comparisons_table('Prueba LSD', lsd, 't crítico')
    comparisons_table('Prueba de Tukey', tukey, 'q crítico')
    comparisons_table('Prueba de Duncan', duncan, 'q crítico')

    html.append("</body></html>")
    return "\n".join(html)


def format_text(groups):
    """Return a plain text report for the ANOVA and post-hoc tests."""
    anova_res = run_anova(groups)
    lsd = calcular_lsd(groups)
    tukey = calcular_tukey(groups)
    duncan = calcular_duncan(groups)
    shapiro = prueba_shapiro(groups)
    bartlett = prueba_bartlett(groups)

    lines = ["MEDIAS POR GRUPO"]
    for g, m in anova_res["group_means"].items():
        lines.append(f"  {g}: {m:.4f}")

    lines.append("\nTABLA ANOVA (FV, SC, GL, CM, F0, Valor-p)")
    lines.append(
        f"Tratamientos: {anova_res['SC_TRAT']:.4f}, {anova_res['GL_TRAT']}, {anova_res['CM_TRAT']:.4f}, {anova_res['F0']:.4f}, {anova_res['p_value']:.4f}"
    )
    lines.append(
        f"Error: {anova_res['SC_E']:.4f}, {anova_res['GL_E']}, {anova_res['CM_E']:.4f}"
    )
    lines.append(f"Total: {anova_res['SC_T']:.4f}, {anova_res['GL_T']}")

    lines.append("\nPrueba de normalidad (Shapiro-Wilk)")
    lines.append(
        f"n={shapiro['n']}, W={shapiro['w']:.4f}, p-value={shapiro['p_value']:.4f}"
    )
    lines.append("i\tai\tX(n-i+1)-X(i)\tai*(X(n-i+1)-X(i))")
    for fila in shapiro['tabla']:
        lines.append(
            f"{fila['i']}\t{fila['ai']:.4f}\t{fila['diff']:.4f}\t{fila['ai_diff']:.4f}"
        )

    lines.append("\nPrueba de homogeneidad de varianzas (Bartlett)")
    lines.append(
        f"k={bartlett['k']}, chi2={bartlett['chi2']:.4f}, p-value={bartlett['p_value']:.4f}"
    )
    lines.append("Grupo\tni\tVarianza")
    for fila in bartlett['tabla']:
        lines.append(f"{fila['grupo']}\t{fila['n']}\t{fila['var']:.4f}")

    def comps(title, res, key):
        lines.append(f"\n{title}")
        for comp in res["comparaciones"].values():
            crit = comp.get("t_crit") or comp.get("q_crit")
            val = comp.get(key)
            sig = "Sí" if comp["significant"] else "No"
            lines.append(
                f"  {comp['grupo1']} - {comp['grupo2']}: diff={comp['diff']:.4f}, se={comp['se']:.4f}, crit={crit:.4f}, {key}={val:.4f}, sig={sig}"
            )

    comps("Prueba LSD", lsd, "lsd")
    comps("Prueba de Tukey", tukey, "hsd")
    comps("Prueba de Duncan", duncan, "dms")

    return "\n".join(lines)


def main():
    # Datos de ejemplo equivalentes a los que se encontraban en la página HTML
    groups = {
        "A": [6, 8, 7, 8],
        "B": [7, 9, 10, 8],
        "C": [11, 16, 11, 13],
        "D": [10, 12, 11, 9],
    }

    html = generate_html(groups)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Archivo index.html generado con los resultados")


if __name__ == "__main__":
    main()
