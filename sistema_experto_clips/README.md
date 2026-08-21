# Sistema Experto - ¿A dónde ir de vacaciones? (CLIPSPY)

Sistema experto basado en reglas que recomienda un destino de vacaciones
según las preferencias del usuario: presupuesto, clima, compañía, duración
del viaje y tipo de actividad deseada.

## Tecnologías
- **CLIPSPY**: motor de inferencia (reglas CLIPS ejecutadas desde Python).
- **tkinter**: interfaz gráfica de usuario.

## Estructura
- `motor_reglas.py`: contiene la base de conocimiento (7 reglas CLIPS) y la
  función `recomendar()` que ejecuta el motor de inferencia.
- `app_gui.py`: interfaz gráfica (formulario con listas desplegables) que
  llama al motor de reglas y muestra el resultado.

## Base de reglas (7 reglas, mínimo 5)
1. `regla-playa-lujo`: presupuesto alto + clima cálido + relax → playa de lujo.
2. `regla-cultura-economica`: presupuesto bajo + clima templado + cultura → pueblo colonial / eje cafetero.
3. `regla-montana-aventura`: clima frío + aventura → destino de montaña.
4. `regla-familiar`: viaje en familia + duración media + relax → destino familiar.
5. `regla-amigos-fiesta`: viaje con amigos + fiesta → destino de rumba.
6. `regla-escapada-corta`: presupuesto bajo + duración corta → escapada cercana.
7. `regla-default` (salience -100): se activa solo si ninguna otra regla aplicó.

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

Pruebas de consola del motor de reglas (sin GUI):
```bash
python3 motor_reglas.py
```

## Ejemplo de uso
1. Selecciona tu presupuesto, clima preferido, con quién viajas, duración
   del viaje y tipo de actividad.
2. Presiona **"Recomendar destino"**.
3. El sistema experto muestra el destino sugerido, una descripción y la
   regla CLIPS que se activó.
