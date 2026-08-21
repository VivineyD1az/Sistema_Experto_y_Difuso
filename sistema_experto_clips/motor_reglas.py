"""
Motor de reglas del Sistema Experto de Vacaciones (CLIPSPY).

Este módulo contiene únicamente la lógica del sistema experto,
separada de la interfaz gráfica, para poder probarla de forma
independiente.
"""

import clips


REGLAS_CLIPS = """
(deftemplate preferencia
   (slot presupuesto)   ; bajo | medio | alto
   (slot clima)          ; frio | templado | calido
   (slot compania)        ; solo | pareja | familia | amigos
   (slot duracion)         ; corta | media | larga
   (slot actividad))        ; relax | aventura | cultura | fiesta

(deftemplate recomendacion
   (slot destino)
   (slot descripcion)
   (slot regla))

;; Regla 1: viajero con alto presupuesto que busca playa y relax
(defrule regla-playa-lujo
   (preferencia (presupuesto alto) (clima calido) (actividad relax))
   =>
   (assert (recomendacion
              (destino "Cartagena / Maldivas")
              (descripcion "Playas de lujo y resorts todo incluido, ideales para desconectarse con un presupuesto alto.")
              (regla "regla-playa-lujo"))))

;; Regla 2: presupuesto bajo, clima templado, interés cultural
(defrule regla-cultura-economica
   (preferencia (presupuesto bajo) (clima templado) (actividad cultura))
   =>
   (assert (recomendacion
              (destino "Villa de Leyva / Eje Cafetero")
              (descripcion "Pueblos coloniales y paisajes cafeteros: experiencia cultural económica.")
              (regla "regla-cultura-economica"))))

;; Regla 3: clima frio con ganas de aventura
(defrule regla-montana-aventura
   (preferencia (clima frio) (actividad aventura))
   =>
   (assert (recomendacion
              (destino "Nevado del Ruiz / San Gil")
              (descripcion "Destinos de montaña y clima frío, perfectos para deportes de aventura.")
              (regla "regla-montana-aventura"))))

;; Regla 4: viaje familiar de duración media enfocado en relax
(defrule regla-familiar
   (preferencia (compania familia) (duracion media) (actividad relax))
   =>
   (assert (recomendacion
              (destino "San Andrés")
              (descripcion "Playas tranquilas y planes familiares en un viaje de duración media.")
              (regla "regla-familiar"))))

;; Regla 5: viaje entre amigos enfocado en fiesta
(defrule regla-amigos-fiesta
   (preferencia (compania amigos) (actividad fiesta))
   =>
   (assert (recomendacion
              (destino "Medellín / Cartagena (centro histórico)")
              (descripcion "Vida nocturna y planes grupales para disfrutar en compañía de amigos.")
              (regla "regla-amigos-fiesta"))))

;; Regla 6: escapada corta y económica
(defrule regla-escapada-corta
   (preferencia (presupuesto bajo) (duracion corta))
   =>
   (assert (recomendacion
              (destino "Guatapé")
              (descripcion "Escapada corta, cercana y económica, ideal para un fin de semana.")
              (regla "regla-escapada-corta"))))

;; Regla 7 (por defecto): si ninguna regla anterior aplicó
(defrule regla-default
   (declare (salience -100))
   (preferencia)
   (not (recomendacion))
   =>
   (assert (recomendacion
              (destino "Eje Cafetero")
              (descripcion "Destino versátil: combina naturaleza, cultura y buen clima para cualquier perfil de viajero.")
              (regla "regla-default"))))
"""


def crear_motor():
    """Crea y construye un entorno CLIPS con las reglas del sistema.

    clips.Environment.build() solo admite una construcción (deftemplate,
    defrule, etc.) por llamada, así que separamos el texto en bloques
    balanceados por paréntesis y construimos cada uno por separado.
    """
    env = clips.Environment()
    for construccion in _dividir_construcciones(REGLAS_CLIPS):
        env.build(construccion)
    return env


def _dividir_construcciones(texto):
    """Divide un bloque de texto CLIPS en construcciones top-level,
    balanceando paréntesis e ignorando comentarios que empiezan con ';'."""
    construcciones = []
    buffer = []
    profundidad = 0
    dentro = False

    for linea in texto.splitlines():
        # eliminar comentarios de línea completa o al final de línea
        if ";" in linea:
            linea = linea.split(";", 1)[0]
        if not linea.strip() and not dentro:
            continue
        buffer.append(linea)
        profundidad += linea.count("(") - linea.count(")")
        dentro = True
        if dentro and profundidad == 0:
            construcciones.append("\n".join(buffer))
            buffer = []
            dentro = False

    return [c for c in construcciones if c.strip()]


def recomendar(presupuesto, clima, compania, duracion, actividad):
    """
    Ejecuta el sistema experto con las preferencias dadas y devuelve
    una lista de diccionarios con las recomendaciones generadas.

    Cada parámetro debe ser uno de los valores permitidos (ver arriba).
    """
    env = crear_motor()
    env.reset()

    hecho = (
        f'(preferencia (presupuesto {presupuesto}) (clima {clima}) '
        f'(compania {compania}) (duracion {duracion}) (actividad {actividad}))'
    )
    env.assert_string(hecho)
    env.run()

    resultados = []
    for fact in env.facts():
        if fact.template is not None and fact.template.name == "recomendacion":
            resultados.append({
                "destino": fact["destino"],
                "descripcion": fact["descripcion"],
                "regla": fact["regla"],
            })
    return resultados


if __name__ == "__main__":
    # Pruebas rápidas de consola (sin GUI)
    casos = [
        ("alto", "calido", "pareja", "media", "relax"),
        ("bajo", "templado", "solo", "larga", "cultura"),
        ("medio", "frio", "amigos", "media", "aventura"),
        ("medio", "templado", "familia", "media", "relax"),
        ("alto", "calido", "amigos", "corta", "fiesta"),
        ("bajo", "calido", "solo", "corta", "relax"),
    ]
    for caso in casos:
        print("Preferencias:", caso)
        for r in recomendar(*caso):
            print("  ->", r["destino"], "|", r["regla"])
        print()
