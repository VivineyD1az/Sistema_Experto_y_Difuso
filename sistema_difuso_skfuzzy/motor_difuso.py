"""
Motor de razonamiento difuso del Sistema de Vacaciones (SKFuzzy).

Determina cuántos días de vacaciones se recomienda tomar, a partir de:
  - nivel de estrés (0-10)
  - carga laboral / desgaste acumulado (0-10)
  - presupuesto disponible (0-10)

Salida:
  - dias_vacaciones (0-20 días recomendados)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ---------------------------------------------------------------------------
# Variables lingüísticas (universos de discurso)
# ---------------------------------------------------------------------------
estres = ctrl.Antecedent(np.arange(0, 11, 1), "estres")
carga_laboral = ctrl.Antecedent(np.arange(0, 11, 1), "carga_laboral")
presupuesto = ctrl.Antecedent(np.arange(0, 11, 1), "presupuesto")

dias_vacaciones = ctrl.Consequent(np.arange(0, 21, 1), "dias_vacaciones")

# Funciones de membresía - Entradas
estres["bajo"] = fuzz.trimf(estres.universe, [0, 0, 5])
estres["medio"] = fuzz.trimf(estres.universe, [2, 5, 8])
estres["alto"] = fuzz.trimf(estres.universe, [5, 10, 10])

carga_laboral["baja"] = fuzz.trimf(carga_laboral.universe, [0, 0, 5])
carga_laboral["media"] = fuzz.trimf(carga_laboral.universe, [2, 5, 8])
carga_laboral["alta"] = fuzz.trimf(carga_laboral.universe, [5, 10, 10])

presupuesto["bajo"] = fuzz.trimf(presupuesto.universe, [0, 0, 5])
presupuesto["medio"] = fuzz.trimf(presupuesto.universe, [2, 5, 8])
presupuesto["alto"] = fuzz.trimf(presupuesto.universe, [5, 10, 10])

# Funciones de membresía - Salida
dias_vacaciones["pocos"] = fuzz.trimf(dias_vacaciones.universe, [0, 0, 7])
dias_vacaciones["moderados"] = fuzz.trimf(dias_vacaciones.universe, [4, 10, 16])
dias_vacaciones["muchos"] = fuzz.trimf(dias_vacaciones.universe, [12, 20, 20])


# ---------------------------------------------------------------------------
# Base de reglas difusas (mínimo 5 reglas)
# ---------------------------------------------------------------------------
regla1 = ctrl.Rule(estres["alto"] & carga_laboral["alta"], dias_vacaciones["muchos"])
regla2 = ctrl.Rule(estres["bajo"] & carga_laboral["baja"], dias_vacaciones["pocos"])
regla3 = ctrl.Rule(presupuesto["bajo"], dias_vacaciones["pocos"])
regla4 = ctrl.Rule(estres["medio"] & presupuesto["medio"], dias_vacaciones["moderados"])
regla5 = ctrl.Rule(presupuesto["alto"] & estres["alto"], dias_vacaciones["muchos"])
regla6 = ctrl.Rule(carga_laboral["media"] & presupuesto["medio"], dias_vacaciones["moderados"])
regla7 = ctrl.Rule(estres["bajo"] & presupuesto["alto"], dias_vacaciones["moderados"])

REGLAS = [regla1, regla2, regla3, regla4, regla5, regla6, regla7]


def crear_sistema():
    """Crea el sistema de control difuso a partir de la base de reglas."""
    sistema_ctrl = ctrl.ControlSystem(REGLAS)
    return ctrl.ControlSystemSimulation(sistema_ctrl)


def evaluar(nivel_estres, nivel_carga, nivel_presupuesto):
    """
    Ejecuta el sistema difuso con valores crisp de entrada (0-10) y
    devuelve un diccionario con:
      - dias_recomendados: valor defuzzificado (float)
      - urgencia: etiqueta cualitativa según el resultado
    """
    simulacion = crear_sistema()
    simulacion.input["estres"] = nivel_estres
    simulacion.input["carga_laboral"] = nivel_carga
    simulacion.input["presupuesto"] = nivel_presupuesto
    simulacion.compute()

    dias = simulacion.output["dias_vacaciones"]
    dias_enteros = round(dias)

    if dias_enteros < 6:
        urgencia = "Baja - puedes esperar un poco más para tomar tus vacaciones"
    elif dias_enteros < 13:
        urgencia = "Media - te conviene planear un viaje pronto"
    else:
        urgencia = "Alta - necesitas descansar cuanto antes"

    return {
        "dias_recomendados": dias_enteros,
        "dias_exacto": round(float(dias), 1),
        "urgencia": urgencia,
        "simulacion": simulacion,
    }


if __name__ == "__main__":
    casos = [
        (9, 9, 8, "Muy estresado, mucha carga, buen presupuesto"),
        (1, 1, 2, "Relajado, poca carga, presupuesto bajo"),
        (5, 5, 5, "Todo en valores medios"),
        (2, 3, 9, "Poco estrés pero buen presupuesto"),
        (8, 4, 1, "Alto estrés pero presupuesto muy bajo"),
    ]
    for e, c, p, descripcion in casos:
        r = evaluar(e, c, p)
        print(f"{descripcion}")
        print(f"  estres={e}, carga={c}, presupuesto={p} -> "
              f"{r['dias_recomendados']} días (exacto: {r['dias_exacto']}) | "
              f"Urgencia: {r['urgencia']}\n")