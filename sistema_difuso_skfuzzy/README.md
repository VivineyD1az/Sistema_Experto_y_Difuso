# Sistema Difuso - ¿Cuántos días de vacaciones tomar? (SKFuzzy)

Sistema de razonamiento difuso que estima cuántos días de vacaciones se
recomienda tomar y qué tan urgente es descansar, a partir de tres variables:
nivel de estrés, carga laboral acumulada y presupuesto disponible.

## Tecnologías
- **scikit-fuzzy (skfuzzy)**: variables lingüísticas, funciones de membresía,
  base de reglas difusas e inferencia Mamdani con defuzzificación (centroide).
- **tkinter + matplotlib**: interfaz gráfica con sliders y gráfico de la
  variable de salida.

## Estructura
- `motor_difuso.py`: define las variables de entrada/salida, las funciones
  de membresía y la base de reglas (7 reglas). Expone la función `evaluar()`.
- `app_gui.py`: interfaz gráfica con sliders para las 3 entradas, botón de
  cálculo y gráfico embebido de las funciones de membresía de salida con el
  valor defuzzificado marcado.

## Variables

**Entradas (universo 0-10):**
- `estres`: bajo / medio / alto
- `carga_laboral`: baja / media / alta
- `presupuesto`: bajo / medio / alto

**Salida (universo 0-20 días):**
- `dias_vacaciones`: pocos / moderados / muchos

## Base de reglas (7 reglas, mínimo 5)
1. Si estrés es alto y carga laboral es alta → muchos días.
2. Si estrés es bajo y carga laboral es baja → pocos días.
3. Si presupuesto es bajo → pocos días.
4. Si estrés es medio y presupuesto es medio → días moderados.
5. Si presupuesto es alto y estrés es alto → muchos días.
6. Si carga laboral es media y presupuesto es medio → días moderados.
7. Si estrés es bajo y presupuesto es alto → días moderados.

## Instalación
```bash
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **Nota:** `tkinter` viene incluido con Python en la mayoría de instalaciones.
> Si no está disponible en Linux, instálalo con:
> `sudo apt install python3-tk`

## Ejecución

Interfaz gráfica:
```bash
python3 app_gui.py
```

Pruebas de consola del motor difuso (sin GUI):
```bash
python3 motor_difuso.py
```

## Ejemplo de uso
1. Ajusta los sliders de estrés, carga laboral y presupuesto (0 a 10).
2. Presiona **"Calcular días de vacaciones"**.
3. El sistema muestra los días recomendados, el nivel de urgencia y un
   gráfico con las funciones de membresía de salida y el valor calculado.
