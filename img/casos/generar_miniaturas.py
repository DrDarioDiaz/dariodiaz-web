"""Genera las miniaturas (1200x750) de los casos del portfolio con la paleta del sitio.

Las cifras provienen de los resultados de cada caso renderizado; si un caso cambia,
actualizar los valores y volver a ejecutar:  python img/casos/generar_miniaturas.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

TINTA, SUAVE, SELVA, TIERRA, PAPEL, GRIS = "#1c2733", "#4a5866", "#1f6f57", "#b4532a", "#fbfaf7", "#9aa5b1"
DESTINO = Path(__file__).parent
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 15, "axes.edgecolor": SUAVE,
                     "axes.labelcolor": SUAVE, "xtick.color": SUAVE, "ytick.color": SUAVE})


def lienzo():
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
    fig.patch.set_facecolor(PAPEL)
    ax.set_facecolor(PAPEL)
    ax.spines[["top", "right"]].set_visible(False)
    return fig, ax


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(DESTINO / nombre, facecolor=PAPEL)
    plt.close(fig)


# 1. Diseño muestral: respuestas necesarias para la misma precisión
fig, ax = lienzo()
disenos = ["Aleatorio\nsimple", "Estratificado\nproporcional", "Estratificado\nNeyman"]
n = [2529, 1857, 487]
barras = ax.bar(disenos, n, color=[GRIS, TIERRA, SELVA], width=0.62)
ax.bar_label(barras, labels=[f"{v:,}".replace(",", ".") for v in n], padding=6,
             fontsize=20, fontweight="bold", color=TINTA)
ax.set_ylim(0, 2950)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_title("Respuestas necesarias para un error del ±5 %", loc="left", color=SUAVE, fontsize=15, pad=12)
guardar(fig, "diseno-muestral.png")

# 2. Encuesta ponderada: cobertura real de los intervalos del 95 %
fig, ax = lienzo()
metodos = ["Según el\ndiseño", "Sin\nponderar"]
cob = [0.94, 0.62]
barras = ax.barh(metodos, cob, color=[SELVA, GRIS], height=0.55)
ax.axvline(0.95, color=TIERRA, linestyle="--", linewidth=2)
ax.text(0.94, -0.48, "95 % prometido", color=TIERRA, ha="right", va="center", fontsize=14, fontweight="bold")
ax.bar_label(barras, labels=[f"{100*v:.0f} %" for v in cob], padding=10, fontsize=22, fontweight="bold", color=TINTA)
ax.set_xlim(0, 1.2)
ax.set_ylim(-0.7, 1.45)
ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.set_title("Cobertura real de un intervalo del 95 %", loc="left", color=SUAVE, fontsize=15, pad=12)
guardar(fig, "encuesta-ponderada.png")

# 3. Cuestionario: efecto ilustrativo de una pregunta inductiva (Likert apilado)
fig, ax = lienzo()
categorias = ["Muy en desac.", "En desac.", "Neutral", "De acuerdo", "Muy de ac."]
colores = ["#8f3d1c", "#d98b62", "#d9d4ca", "#6aa58c", SELVA]
datos = {"Pregunta\nneutral": [9, 18, 24, 33, 16], "Pregunta\ninductiva": [3, 7, 10, 42, 38]}
for i, (etiqueta, valores) in enumerate(datos.items()):
    izq = 0
    for v, c in zip(valores, colores):
        ax.barh(i, v, left=izq, color=c, height=0.55, edgecolor=PAPEL, linewidth=2)
        if v >= 9:
            ax.text(izq + v / 2, i, f"{v} %", ha="center", va="center", fontsize=14,
                    color="white" if c != "#d9d4ca" else TINTA, fontweight="bold")
        izq += v
ax.set_yticks([0, 1], list(datos))
ax.set_xlim(0, 100)
ax.set_xticks([])
ax.spines[["bottom", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.set_title("Misma pregunta, distinta redacción (ilustrativo)", loc="left", color=SUAVE, fontsize=15, pad=12)
ax.legend([plt.Rectangle((0, 0), 1, 1, color=c) for c in colores],
          [c.replace("\n", " ") for c in categorias], ncol=5, frameon=False, fontsize=12, columnspacing=1.0,
          loc="lower center", bbox_to_anchor=(0.5, -0.18), handlelength=1)
guardar(fig, "cuestionario.png")

print("Miniaturas generadas en", DESTINO)
