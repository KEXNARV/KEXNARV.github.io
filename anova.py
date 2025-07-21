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
    GL_TRAT = k - 1
    GL_E = N - k
    GL_T = N - 1
    CM_TRAT = SC_TRAT / GL_TRAT
    CM_E = SC_E / GL_E
    F0 = CM_TRAT / CM_E
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
