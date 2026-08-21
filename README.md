# Proyecto de IA: ayudarme a elegir mis vacaciones

Para este trabajo teniamos que construir dos sistemas, cada uno con una librería específica y mínimo 5 reglas. Decidí
usar el mismo tema para los dos —elegir mis vacaciones— pero resolviendo
preguntas diferentes con cada técnica.

## Punto 1: Sistema Experto con CLIPSPY

📂 `sistema_experto_clips/`

Este sistema responde: **¿a qué destino debería ir?**

Le doy mis preferencias (presupuesto, clima que prefiero, con quién viajo,
cuánto tiempo tengo y qué actividad busco) y un motor de reglas CLIPS
evalúa esa información contra una base de conocimiento y me devuelve un
destino recomendado con su justificación.

Tiene 7 reglas (pedían mínimo 5). Por ejemplo: si tengo presupuesto alto,
me gusta el clima cálido y quiero relajarme, la regla me recomienda un
destino de playa; si voy con amigos y busco fiesta, me recomienda un
destino con buena vida nocturna. También agregué una regla "por defecto"
que solo se activa si ninguna de las otras aplicó, para que el sistema
siempre dé una respuesta.

Elegí CLIPS para esto porque el problema es de tipo "si se cumplen estas
condiciones exactas, entonces esta conclusión" — encaja bien con reglas
lógicas claras, sin ambigüedad.

## Punto 2: Sistema de Razonamiento Difuso con SKFuzzy

📂 `sistema_difuso_skfuzzy/`

Este sistema responde: **¿cuántos días de vacaciones debería tomarme?**

Aquí la lógica clásica de "si/entonces" no encajaba tan bien, porque el
estrés o la carga laboral no son valores exactos sino cuestión de grados
(no es lo mismo un estrés de 6 que de 9, y ambos son "altos"). Por eso usé
lógica difusa: le doy tres valores de 0 a 10 (nivel de estrés, carga
laboral acumulada y presupuesto disponible) y el sistema los evalúa con
funciones de membresía (bajo/medio/alto) para calcular cuántos días de
descanso recomienda, con 7 reglas difusas.

El resultado se redondea a un número entero de días (nadie toma "4.4 días"
de vacaciones), pero muestro también el valor exacto antes de redondear
para poder explicar en la sustentación cómo funciona la defuzzificación
por centroide.

## Cómo está organizado cada sistema

En ambas carpetas separé la lógica de la interfaz para poder explicar cada
parte por separado en la sustentación:

- `motor_reglas.py` / `motor_difuso.py`: toda la base de conocimiento
  (reglas, variables, funciones de membresía). Se puede correr solo por
  consola para probar el motor sin la interfaz gráfica.
- `app_gui.py`: la interfaz gráfica (tkinter) que le pide los datos al
  usuario, llama al motor y muestra el resultado.
- `README.md` propio con el detalle de las reglas y cómo instalar/correr.
- `requirements.txt` con las librerías que necesita cada uno.

## Cómo correrlos (paso a paso)

### 1. Requisitos previos

- Tener **Python** instalado (versión 3.10 o superior). Se puede verificar
  abriendo una terminal y ejecutando:
  ```bash
  python --version
  ```
- Tener **Git** instalado, si vas a clonar el repositorio.
- **Windows:** usar PowerShell o la terminal integrada de VS Code.

### 2. Clonar o descargar el proyecto

```bash
git clone https://github.com/TU-USUARIO/NOMBRE-DEL-REPO.git
cd NOMBRE-DEL-REPO
```

(O si ya tienes la carpeta descargada/descomprimida, solo entra a ella con `cd`.)

### 3. Crear y activar un entorno virtual

Esto evita instalar las librerías directamente en el sistema.

```bash
python -m venv venv
```

Activarlo:
- **Windows (PowerShell):**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

Cuando está activo, la terminal muestra `(venv)` al inicio de la línea.

### 4. Instalar las dependencias

Cada sistema tiene su propio `requirements.txt`. Con el entorno virtual
activado, instala ambos (o solo el que vayas a correr):

```bash
python -m pip install --upgrade pip
python -m pip install -r sistema_experto_clips/requirements.txt
python -m pip install -r sistema_difuso_skfuzzy/requirements.txt
```

> **Nota:** `tkinter` (la interfaz gráfica) viene incluido con Python en
> Windows y Mac. En Linux, si falta, se instala con:
> `sudo apt install python3-tk`

### 5. Ejecutar el Sistema Experto (CLIPSPY)

```bash
cd sistema_experto_clips
python app_gui.py
```

Se abre una ventana con un formulario: eliges presupuesto, clima, con
quién viajas, duración y tipo de actividad, presionas **"Recomendar
destino"** y el sistema muestra el destino sugerido.

Para probar el motor de reglas sin la interfaz (por consola):
```bash
python motor_reglas.py
```

### 6. Ejecutar el Sistema Difuso (SKFuzzy)

Desde la raíz del proyecto:
```bash
cd sistema_difuso_skfuzzy
python app_gui.py
```

Se abre una ventana con tres sliders (estrés, carga laboral, presupuesto).
Al mover los sliders y presionar **"Calcular días de vacaciones"**, el
sistema muestra los días recomendados y un gráfico con las funciones de
membresía de salida.

Para probar el motor difuso sin la interfaz (por consola):
```bash
python motor_difuso.py
```

### 7. Problemas comunes

- **`pip` no se reconoce como comando:** usar `python -m pip` en su lugar.
- **`ModuleNotFoundError` de scipy, networkx, etc.:** instalar el paquete
  faltante manualmente, ej. `python -m pip install scipy networkx`.
- **La ventana no abre / error de tkinter en Linux:** instalar
  `python3-tk` con el gestor de paquetes del sistema.
- **`clipspy` no instala:** verificar la versión de Python; CLIPSPY
  requiere una versión con wheel precompilado disponible (revisar
  [PyPI de clipspy](https://pypi.org/project/clipspy/) para compatibilidad).

## Para la sustentación (25 de agosto)

Cosas que quiero tener claras para explicar cada sistema:

- Por qué elegí esas variables de entrada para cada problema.
- Explicar 2-3 reglas en detalle: qué condiciones evalúan y por qué llegan
  a esa conclusión.
- Mostrar la GUI en vivo con distintos valores, incluyendo un caso borde
  (la regla por defecto en el sistema experto, o valores medios en el
  difuso).
- Para el difuso: explicar fuzzificación → evaluación de reglas →
  defuzzificación (centroide), apoyándome en el gráfico de la GUI que
  muestra las funciones de membresía y dónde cae mi resultado.
