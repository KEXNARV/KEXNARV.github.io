from flask import Flask, request, render_template
import math

app = Flask(__name__)

# Ruta para mostrar el formulario
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para calcular la parte A
@app.route("/calcular_a", methods=["POST"])
def calcular_a():
    # Obtener valores del formulario
    c2 = float(request.form["c2"])  # Radio externo
    c1 = float(request.form["c1"])  # Radio interno
    T_BC = float(request.form["T_BC"])  # Torque

    # Cálculo del momento polar de inercia (J)
    J = (math.pi / 2) * (c2**4 - c1**4)

    # Cálculo del esfuerzo cortante máximo
    T_max = (T_BC * c2) / J

    # Cálculo del esfuerzo cortante mínimo
    T_min = T_max * (c1 / c2)

    # Enviar resultados a la plantilla
    return render_template("resultado.html", 
                           parte="Esfuerzos minimo y maximo",
                           titulo="Resultados esfuerzos minimo y maximo",
                           datos=[
                               {"label": "Momento polar de inercia (J)", "valor": f"{J:.6e} m⁴"},
                               {"label": "Esfuerzo cortante máximo (T_max)", "valor": f"{T_max / 1e6:.2f} MPa"},
                               {"label": "Esfuerzo cortante mínimo (T_min)", "valor": f"{T_min / 1e6:.2f} MPa"}
                           ])

# Ruta para calcular la parte B
@app.route("/calcular_b", methods=["POST"])
def calcular_b():
    # Obtener valores del formulario
    T = float(request.form["T"])  # Torque
    tau_perm = float(request.form["tau_perm"]) * 1e6  # Esfuerzo permisible (convertido a Pa)

    # Cálculo del diámetro requerido
    d = ((16 * T) / (math.pi * tau_perm)) ** (1 / 3)

    # Enviar resultados a la plantilla
    return render_template("resultado.html", 
                           parte="diametro requerido",
                           titulo="Resultados diametro requerido",
                           datos=[
                               {"label": "Torque aplicado (T)", "valor": f"{T:.2f} N·m"},
                               {"label": "Esfuerzo cortante permisible (τ)", "valor": f"{tau_perm / 1e6:.2f} MPa"},
                               {"label": "Diámetro requerido (d)", "valor": f"{d:.4f} m ({d * 1000:.2f} mm)"}
                           ])

if __name__ == "__main__":
    app.run(debug=True)
