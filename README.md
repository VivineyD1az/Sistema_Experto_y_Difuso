# Sistemas de Inteligencia Artificial - Vacaciones

Proyecto para la asignatura (UNAC), con dos sistemas independientes, ambos
con interfaz gráfica, sobre el mismo tema: **ayudar a elegir mis vacaciones**.

## Punto 1 — Sistema Experto (CLIPSPY)
📂 `sistema_experto_clips/`
Recomienda **a dónde viajar** según presupuesto, clima, compañía, duración
y tipo de actividad. Motor de reglas CLIPS con 7 reglas (mínimo 5 requerido).

## Punto 2 — Sistema de Razonamiento Difuso (SKFuzzy)
📂 `sistema_difuso_skfuzzy/`
Recomienda **cuántos días de vacaciones tomar** y qué tan urgente es
descansar, según estrés, carga laboral y presupuesto. Base difusa con
7 reglas (mínimo 5 requerido).

Cada carpeta tiene su propio `README.md`, `requirements.txt` y su interfaz
gráfica (`app_gui.py`), separada de la lógica (`motor_reglas.py` /
`motor_difuso.py`) para facilitar la sustentación.

## Cómo subir esto a GitHub

Desde la carpeta `vacaciones-ia/`:

```bash
git init
git add .
git commit -m "Sistema experto CLIPS + sistema difuso SKFuzzy - vacaciones"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/NOMBRE-DEL-REPO.git
git push -u origin main
```

Reemplaza `TU-USUARIO/NOMBRE-DEL-REPO` por la URL de tu repositorio en GitHub
(créalo antes vacío, sin README, desde github.com/new).

## Para la sustentación (25 de agosto)
Ten preparado para cada sistema:
- Explicar qué son las variables/hechos de entrada y de dónde salen.
- Mostrar la base de reglas y explicar 2-3 reglas en detalle (por qué
  esas condiciones producen esa conclusión).
- Ejecutar la GUI en vivo con distintos valores y mostrar cómo cambia
  el resultado, incluyendo un caso borde (ej. la regla por defecto en
  el sistema experto, o valores medios en el difuso).
- Para el sistema difuso: explicar funciones de membresía, fuzzificación,
  evaluación de reglas y defuzzificación (centroide), apoyándote en el
  gráfico de la GUI.
