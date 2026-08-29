# docs/generate_figures.py — génère les visuels du modèle de prévision (SARIMA)
# pour le rapport technique, à partir des mêmes fonctions que le dashboard
# (utils.py::fit_forecast_model). Lancer depuis la racine du repo :
#   python docs/generate_figures.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from utils import fit_forecast_model

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")

# Série de référence pour illustrer le modèle : Urgences - Passages totaux,
# tous sites (PLF+CFX), mode Normal. C'est la série la plus longue et la
# plus lisible pour un public non technique.
DATA_PATH = os.path.join("data", "activity_service", "activity_service-all.csv")
INDICATEUR = "Urgences"
SOUS_INDICATEUR = "Passages totaux"
LABEL = "Urgences — Passages totaux (PLF + CFX), mode Normal"


def load_series():
    df = pd.read_csv(DATA_PATH)
    df = df[(df["indicateur"] == INDICATEUR) & (df["sous_indicateur"] == SOUS_INDICATEUR)]
    return df[["year", "month", "value"]]


def plot_forecast(series, results, out_path):
    forecast = results.get_forecast(steps=12)
    pred = forecast.predicted_mean
    ci = forecast.conf_int(alpha=0.20)  # intervalle de confiance à 80%
    first_year, last_year = series.index[0].year, series.index[-1].year
    forecast_year = last_year + 1

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(series.index, series.values, label=f"Historique ({first_year}-{last_year}, reconstitué)", color="#1F3B57")
    ax.plot(pred.index, pred.values, label=f"Prévision {forecast_year} (SARIMA)", color="#E67E22", linewidth=2)
    ax.fill_between(
        ci.index, ci.iloc[:, 0], ci.iloc[:, 1],
        color="#E67E22", alpha=0.2, label="Intervalle de confiance 80%",
    )
    ax.set_title(f"Prévision SARIMA — {LABEL}")
    ax.set_ylabel("Passages / mois")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"OK {out_path}")


def plot_diagnostics(results, out_path):
    fig = results.plot_diagnostics(figsize=(11, 8))
    fig.suptitle(f"Diagnostics du modèle SARIMA — {LABEL}", y=1.02)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"OK {out_path}")


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    df = load_series()
    series, results = fit_forecast_model(df)
    if series is None:
        print("Pas assez de points mensuels pour ajuster le modèle (besoin de >= 24).")
        return
    plot_forecast(series, results, os.path.join(FIGURES_DIR, "forecast_urgences.png"))
    plot_diagnostics(results, os.path.join(FIGURES_DIR, "forecast_diagnostics.png"))


if __name__ == "__main__":
    main()
