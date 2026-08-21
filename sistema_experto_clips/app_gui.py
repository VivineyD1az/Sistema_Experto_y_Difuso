"""
Sistema Difuso - ¿Cuántos días de vacaciones debería tomar?
Interfaz gráfica con tkinter, lógica difusa con scikit-fuzzy (skfuzzy).

Ejecutar con:  python3 app_gui.py
"""

import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from motor_difuso import evaluar, dias_vacaciones


class VacacionesDifusoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Difuso - ¿Cuántos días de vacaciones tomar? (SKFuzzy)")
        self.root.geometry("760x640")
        self.root.resizable(False, False)

        titulo = ttk.Label(
            root, text="Calculadora difusa de vacaciones",
            font=("Segoe UI", 14, "bold")
        )
        titulo.pack(pady=(15, 0))
        ttk.Label(
            root, text="Mueve los sliders y descubre cuántos días de descanso necesitas",
            font=("Segoe UI", 9)
        ).pack(pady=(0, 10))

        contenedor = ttk.Frame(root)
        contenedor.pack(fill="both", expand=True, padx=20)

        panel_izq = ttk.Frame(contenedor)
        panel_izq.pack(side="left", fill="y", padx=(0, 15))

        self.sliders = {}
        self._crear_slider(panel_izq, "estres", "Nivel de estrés (0-10):", 7)
        self._crear_slider(panel_izq, "carga_laboral", "Carga laboral acumulada (0-10):", 6)
        self._crear_slider(panel_izq, "presupuesto", "Presupuesto disponible (0-10):", 5)

        boton = ttk.Button(panel_izq, text="Calcular días de vacaciones",
                            command=self.calcular)
        boton.pack(pady=20, fill="x")

        self.resultado_var = tk.StringVar(value="Presiona 'Calcular' para ver el resultado.")
        resultado_lbl = ttk.Label(panel_izq, textvariable=self.resultado_var,
                                   font=("Segoe UI", 11, "bold"), wraplength=260,
                                   justify="left")
        resultado_lbl.pack(pady=(5, 0))

        self.urgencia_var = tk.StringVar(value="")
        urgencia_lbl = ttk.Label(panel_izq, textvariable=self.urgencia_var,
                                  font=("Segoe UI", 9), wraplength=260,
                                  justify="left", foreground="#555555")
        urgencia_lbl.pack(pady=(5, 0))

        # Panel derecho: gráfico de la variable de salida
        panel_der = ttk.Frame(contenedor)
        panel_der.pack(side="left", fill="both", expand=True)

        self.fig = Figure(figsize=(4.8, 4.8), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=panel_der)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self._dibujar_membresias(None)

    def _crear_slider(self, parent, clave, texto, valor_inicial):
        ttk.Label(parent, text=texto).pack(anchor="w", pady=(10, 0))
        var = tk.DoubleVar(value=valor_inicial)
        escala = ttk.Scale(parent, from_=0, to=10, orient="horizontal",
                            variable=var, length=260,
                            command=lambda e, k=clave: self._actualizar_valor(k))
        escala.pack(anchor="w")
        valor_lbl = ttk.Label(parent, text=f"{valor_inicial:.1f}")
        valor_lbl.pack(anchor="w")
        self.sliders[clave] = {"var": var, "label": valor_lbl}

    def _actualizar_valor(self, clave):
        var = self.sliders[clave]["var"]
        self.sliders[clave]["label"].configure(text=f"{var.get():.1f}")

    def _dibujar_membresias(self, resultado_valor):
        self.ax.clear()
        universo = dias_vacaciones.universe
        colores = {"pocos": "#4C72B0", "moderados": "#DD8452", "muchos": "#55A868"}

        for etiqueta, mf in dias_vacaciones.terms.items():
            self.ax.plot(universo, mf.mf, label=etiqueta,
                         color=colores.get(etiqueta, None))

        if resultado_valor is not None:
            self.ax.axvline(resultado_valor, color="black", linestyle="--",
                            linewidth=1.5)
            self.ax.text(resultado_valor, 1.02, f"{resultado_valor:.1f} días",
                         ha="center", fontsize=9)

        self.ax.set_title("Variable de salida: días de vacaciones")
        self.ax.set_xlabel("Días")
        self.ax.set_ylabel("Grado de membresía")
        self.ax.set_ylim(0, 1.15)
        self.ax.legend(loc="upper right", fontsize=8)
        self.fig.tight_layout()
        self.canvas.draw()

    def calcular(self):
        e = self.sliders["estres"]["var"].get()
        c = self.sliders["carga_laboral"]["var"].get()
        p = self.sliders["presupuesto"]["var"].get()

        resultado = evaluar(e, c, p)
        dias = resultado["dias_recomendados"]
        dias_exacto = resultado["dias_exacto"]

        self.resultado_var.set(f"Días de vacaciones recomendados: {dias}")
        self.urgencia_var.set(
            f"Nivel de urgencia: {resultado['urgencia']}\n"
            f"(valor difuso exacto antes de redondear: {dias_exacto} días)"
        )

        self._dibujar_membresias(dias_exacto)


def main():
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    VacacionesDifusoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()