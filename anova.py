def run_anova(groups_js):
    """Run one-way ANOVA from a groups mapping.

    The input may come directly from JavaScript via Pyodide. In that case it is
    a JsProxy object with a ``to_py`` method. When called from regular Python it
    can be a normal ``dict``. This helper ensures we always work with a Python
    ``dict``.
    """
    from scipy import stats
    try:
        groups = groups_js.to_py()
    except AttributeError:
        groups = groups_js
    group_names = list(groups.keys())
    k = len(group_names)
    n_i_list = [len(groups[g]) for g in group_names]
    N = sum(n_i_list)
    Y_total = sum(sum(groups[g]) for g in group_names)
    SC_T = sum(y*y for g in group_names for y in groups[g]) - (Y_total**2) / N
    SC_TRAT = sum((sum(groups[g])**2)/len(groups[g]) for g in group_names) - (Y_total**2)/N
    SC_E = SC_T - SC_TRAT
    cm_results = calcular_cuadrados_medios(SC_TRAT, SC_E, k, N)
    GL_TRAT = cm_results['gl_trat']
    GL_E = cm_results['gl_error']
    GL_T = N - 1
    CM_TRAT = cm_results['cm_trat']
    CM_E = cm_results['cm_error']
    F0 = cm_results['f0']
    p_value = stats.f.sf(F0, GL_TRAT, GL_E)
    group_means = {g: sum(groups[g])/len(groups[g]) for g in group_names}
    return {
        'group_means': group_means,
        'SC_TRAT': SC_TRAT,
        'SC_E': SC_E,
        'SC_T': SC_T,
        'GL_TRAT': GL_TRAT,
        'GL_E': GL_E,
        'GL_T': GL_T,
        'CM_TRAT': CM_TRAT,
        'CM_E': CM_E,
        'F0': F0,
        'p_value': p_value,
    }


def calcular_cuadrados_medios(sc_trat, sc_error, k, N):
    """Calcula los cuadrados medios y el estadístico F para ANOVA."""

    gl_trat = k - 1
    gl_error = N - k
    cm_trat = sc_trat / gl_trat
    cm_error = sc_error / gl_error
    f0 = cm_trat / cm_error
    return {
        'gl_trat': gl_trat,
        'gl_error': gl_error,
        'cm_trat': cm_trat,
        'cm_error': cm_error,
        'f0': f0,
    }


def calculos_por_tratamiento(observaciones_js):
    """Calcula estadísticas básicas a partir de las observaciones.

    The input may come from JavaScript via Pyodide, in which case it will be a
    ``JsProxy``.  Handle both that and regular Python ``dict`` input.
    """

    try:
        observaciones = observaciones_js.to_py()
    except AttributeError:
        observaciones = observaciones_js

    # Datos de observaciones por tratamiento (método de ensamble)

    # Paso 1: Calcular el total por tratamiento (Yi·)
    totales_por_tratamiento = {
        k: sum(v) for k, v in observaciones.items()
    }

    # Paso 2: Calcular el número de datos por tratamiento (ni)
    n_por_tratamiento = {
        k: len(v) for k, v in observaciones.items()
    }

    # Paso 3: Calcular la media muestral por tratamiento (Ȳi)
    medias_por_tratamiento = {
        k: sum(v) / len(v) for k, v in observaciones.items()
    }

    # Paso 4: Calcular la suma total de los datos (Y..)
    total_general = sum(sum(v) for v in observaciones.values())

    # Paso 5: Calcular el número total de observaciones (N)
    N = sum(len(v) for v in observaciones.values())

    # Paso 6: Calcular la media global (Ȳ..)
    media_global = total_general / N

    # Paso 7: Calcular las desviaciones respecto a la media global (τ̂i)
    desviaciones_respecto_media_global = {
        k: medias_por_tratamiento[k] - media_global
        for k in observaciones
    }

    # Paso 8: Calcular la suma de los cuadrados de todos los datos
    suma_cuadrados_total = sum(
        y ** 2 for grupo in observaciones.values() for y in grupo
    )

    return {
        'totales_por_tratamiento': totales_por_tratamiento,
        'n_por_tratamiento': n_por_tratamiento,
        'medias_por_tratamiento': medias_por_tratamiento,
        'total_general': total_general,
        'N': N,
        'media_global': media_global,
        'desviaciones_respecto_media_global': desviaciones_respecto_media_global,
        'suma_cuadrados_total': suma_cuadrados_total,
    }


def calcular_lsd(observaciones_js, alpha=0.05):
    """Realiza comparaciones LSD entre todos los pares de tratamientos.

    Parameters
    ----------
    observaciones_js : dict or JsProxy
        Mapeo de tratamientos a listas de observaciones.
    alpha : float, optional
        Nivel de significancia para el cálculo del valor crítico de *t*.
        Por defecto 0.05.

    Returns
    -------
    dict
        Información de las comparaciones por pares. Para cada par de grupos se
        indican la diferencia absoluta de medias, el error estándar, el valor
        crítico de *t*, la LSD calculada y si la diferencia es significativa.
    """

    from itertools import combinations
    from math import sqrt
    from scipy import stats

    try:
        observaciones = observaciones_js.to_py()
    except AttributeError:
        observaciones = observaciones_js

    anova_res = run_anova(observaciones)
    medias = anova_res['group_means']
    n_por_tratamiento = {k: len(v) for k, v in observaciones.items()}
    cm_error = anova_res['CM_E']
    gl_error = anova_res['GL_E']

    t_crit = stats.t.ppf(1 - alpha / 2, gl_error)

    comparaciones = {}
    for g1, g2 in combinations(observaciones.keys(), 2):
        diff = abs(medias[g1] - medias[g2])
        se = sqrt(cm_error * (1 / n_por_tratamiento[g1] + 1 / n_por_tratamiento[g2]))
        lsd = t_crit * se
        comparaciones[f"{g1}-{g2}"] = {
            'grupo1': g1,
            'grupo2': g2,
            'diff': diff,
            'se': se,
            't_crit': t_crit,
            'lsd': lsd,
            # Para evitar que pequeños errores de redondeo marquen una
            # diferencia como significativa, se añade una tolerancia.
            'significant': diff + 1e-12 >= lsd,
        }

    return {
        't_crit': t_crit,
        'comparaciones': comparaciones,
    }


def calcular_tukey(observaciones_js, alpha=0.05):
    """Realiza la prueba de comparaciones múltiples de Tukey (HSD).

    Parameters
    ----------
    observaciones_js : dict or JsProxy
        Mapeo de tratamientos a listas de observaciones.
    alpha : float, optional
        Nivel de significancia utilizado para obtener el valor crítico
        de la distribución del rango studentizado. Por defecto 0.05.

    Returns
    -------
    dict
        Información de las comparaciones por pares. Para cada par de grupos se
        indican la diferencia absoluta de medias, el error estándar, el valor
        crítico *q*, la HSD calculada y si la diferencia es significativa.
    """

    from itertools import combinations
    from math import sqrt
    from scipy import stats

    try:
        observaciones = observaciones_js.to_py()
    except AttributeError:
        observaciones = observaciones_js

    anova_res = run_anova(observaciones)
    medias = anova_res['group_means']
    n_por_tratamiento = {k: len(v) for k, v in observaciones.items()}
    cm_error = anova_res['CM_E']
    gl_error = anova_res['GL_E']

    k = len(observaciones)
    q_crit = stats.studentized_range.ppf(1 - alpha, k, gl_error)

    comparaciones = {}
    for g1, g2 in combinations(observaciones.keys(), 2):
        diff = abs(medias[g1] - medias[g2])
        se = sqrt(cm_error / 2 * (1 / n_por_tratamiento[g1] + 1 / n_por_tratamiento[g2]))
        hsd = q_crit * se
        comparaciones[f"{g1}-{g2}"] = {
            'grupo1': g1,
            'grupo2': g2,
            'diff': diff,
            'se': se,
            'q_crit': q_crit,
            'hsd': hsd,
            # Diferencia significativa cuando |Ȳi - Ȳj| >= HSD
            'significant': diff >= hsd,
        }

    return {
        'q_crit': q_crit,
        'comparaciones': comparaciones,
    }


def calcular_duncan(observaciones_js, alpha=0.05):
    """Realiza la prueba de comparaciones múltiples de Duncan.

    Parameters
    ----------
    observaciones_js : dict or JsProxy
        Mapeo de tratamientos a listas de observaciones.
    alpha : float, optional
        Nivel de significancia utilizado para obtener el valor crítico
        de la distribución del rango studentizado. Por defecto 0.05.

    Returns
    -------
    dict
        Información de las comparaciones por pares. Para cada par de grupos se
        indican la diferencia absoluta de medias, el error estándar, el valor
        crítico *q*, la DMS calculada y si la diferencia es significativa.
    """

    from itertools import combinations
    from math import sqrt
    from scipy import stats

    try:
        observaciones = observaciones_js.to_py()
    except AttributeError:
        observaciones = observaciones_js

    anova_res = run_anova(observaciones)
    medias = anova_res['group_means']
    n_por_tratamiento = {k: len(v) for k, v in observaciones.items()}
    cm_error = anova_res['CM_E']
    gl_error = anova_res['GL_E']

    # Ordenar los grupos por su media para calcular el rango apropiado
    ordenados = sorted(medias.items(), key=lambda x: x[1])
    orden = [g for g, _ in ordenados]

    comparaciones = {}
    for i in range(len(orden)):
        for j in range(i + 1, len(orden)):
            g1 = orden[i]
            g2 = orden[j]
            diff = abs(medias[g1] - medias[g2])
            r = j - i + 1
            q_crit = stats.studentized_range.ppf(1 - alpha, r, gl_error)
            se = sqrt(cm_error / 2 * (1 / n_por_tratamiento[g1] + 1 / n_por_tratamiento[g2]))
            dms = q_crit * se
            comparaciones[f"{g1}-{g2}"] = {
                'grupo1': g1,
                'grupo2': g2,
                'diff': diff,
                'se': se,
                'q_crit': q_crit,
                'dms': dms,
                'rango': r,
                'significant': diff >= dms,
            }

    return {
        'comparaciones': comparaciones,
    }
