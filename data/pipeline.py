# pipeline.py — fonctions communes réutilisées par chaque domaine :
#   1) interpolate_annual()  : comble les années manquantes (interpolation linéaire)
#   2) apply_crisis()        : simule une crise sanitaire (coefficient multiplicatif)
#   3) reconstruct_monthly() : répartit la valeur annuelle sur 12 mois selon un profil
#                              de saisonnalité assumé (hypothèse documentée)
#
# Toutes les hypothèses (coefficients, % mensuels) sont des paramètres explicites,
# à justifier dans le rapport technique — ce ne sont PAS des données réelles.

import pandas as pd
import numpy as np


def to_number(x):
    if pd.isna(x) or x == "":
        return np.nan
    if isinstance(x, (int, float)):
        return float(x)
    x = str(x).replace("\u202f", "").replace(" ", "").replace(",", ".")
    try:
        return float(x)
    except ValueError:
        return np.nan


def interpolate_annual(df_raw: pd.DataFrame, year_min=2011, year_max=2017) -> pd.DataFrame:
    """Reconstitue une valeur pour chaque année [year_min, year_max] par indicateur/
    sous-indicateur, en interpolant PLF/CFX/TOTAL linéairement entre les points connus.
    Extrapole aux bornes par prolongement de la valeur la plus proche (limit_direction='both')."""
    df = df_raw.copy()
    for col in ["PLF", "CFX", "TOTAL"]:
        df[col] = df[col].apply(to_number)

    out = []
    for (indic, sous), g in df.groupby(["INDICATEUR", "SOUS-INDICATEUR"]):
        unite = g["UNITE"].dropna().iloc[0] if g["UNITE"].notna().any() else ""

        # ratio PLF / (PLF+CFX) médian quand connu, pour répartir un TOTAL isolé
        mask_known = g["PLF"].notna() & g["CFX"].notna() & ((g["PLF"] + g["CFX"]) > 0)
        ratio = (g.loc[mask_known, "PLF"] / (g.loc[mask_known, "PLF"] + g.loc[mask_known, "CFX"])).median() \
            if mask_known.any() else 0.5

        g = g.set_index("ANNEE").reindex(range(year_min, year_max + 1))
        g["INDICATEUR"] = indic
        g["SOUS-INDICATEUR"] = sous
        g["UNITE"] = unite

        # 1) reconstruire PLF/CFX depuis TOTAL quand un seul manque
        m = g["TOTAL"].notna() & g["PLF"].notna() & g["CFX"].isna()
        g.loc[m, "CFX"] = g.loc[m, "TOTAL"] - g.loc[m, "PLF"]
        m = g["TOTAL"].notna() & g["CFX"].notna() & g["PLF"].isna()
        g.loc[m, "PLF"] = g.loc[m, "TOTAL"] - g.loc[m, "CFX"]
        # 2) reconstruire PLF/CFX depuis TOTAL via ratio quand les deux manquent
        m = g["TOTAL"].notna() & g["PLF"].isna() & g["CFX"].isna()
        g.loc[m, "PLF"] = g.loc[m, "TOTAL"] * ratio
        g.loc[m, "CFX"] = g.loc[m, "TOTAL"] * (1 - ratio)

        # 3) interpolation linéaire + extrapolation aux bornes
        g["PLF"] = g["PLF"].interpolate(method="linear", limit_direction="both")
        g["CFX"] = g["CFX"].interpolate(method="linear", limit_direction="both")

        # 4) recompléter TOTAL
        g["TOTAL"] = g["PLF"] + g["CFX"]
        g[["PLF", "CFX", "TOTAL"]] = g[["PLF", "CFX", "TOTAL"]].round(2)

        out.append(g.reset_index().rename(columns={"index": "ANNEE"}))

    return pd.concat(out, ignore_index=True)


def apply_crisis(df_interp: pd.DataFrame, coef: float, note: str = "") -> pd.DataFrame:
    """Ajoute les colonnes PLF_CRISE / CFX_CRISE / TOTAL_CRISE en appliquant un
    coefficient multiplicatif unique (hypothèse simplificatrice de type +X% d'activité
    en période de crise sanitaire)."""
    df = df_interp.copy()
    df["COEF_CRISE"] = coef
    df["HYPOTHESE_CRISE"] = note
    for col in ["PLF", "CFX", "TOTAL"]:
        df[f"{col}_CRISE"] = (df[col] * coef).round(2)
    return df


# Profil mensuel "normal" par défaut : légère sur-activité hivernale (grippe,
# décompensations) + petit pic estival (traumatologie/canicule). Doit sommer à 100.
DEFAULT_MONTH_PCT_NORMAL = {
    1: 10, 2: 9, 3: 8, 4: 7.5, 5: 7, 6: 7,
    7: 8.5, 8: 8, 9: 7.5, 10: 7.5, 11: 8, 12: 12,
}

# Profil mensuel "crise" (type vague épidémique COVID) : creux en début d'année,
# montée brutale au printemps, rechute, deuxième vague à l'automne.
DEFAULT_MONTH_PCT_CRISE = {
    1: 6, 2: 5, 3: 14, 4: 19, 5: 9, 6: 4,
    7: 3, 8: 3, 9: 6, 10: 11, 11: 12, 12: 8,
}


def _check_100(pct: dict, label: str):
    total = sum(pct.values())
    if abs(total - 100) > 0.01:
        raise ValueError(f"{label} doit sommer à 100 (actuel={total})")


def reconstruct_monthly(
    df_crisis: pd.DataFrame,
    month_pct_normal: dict = None,
    month_pct_crisis: dict = None,
) -> pd.DataFrame:
    """Répartit chaque valeur annuelle (normale et crise) sur les 12 mois selon un
    profil de saisonnalité assumé. Retourne un DataFrame long :
    year, month, site_code, indicateur, sous_indicateur, unite, value, value_crise
    """
    month_pct_normal = month_pct_normal or DEFAULT_MONTH_PCT_NORMAL
    month_pct_crisis = month_pct_crisis or DEFAULT_MONTH_PCT_CRISE
    _check_100(month_pct_normal, "month_pct_normal")
    _check_100(month_pct_crisis, "month_pct_crisis")

    rows = []
    for _, r in df_crisis.iterrows():
        for site, col_n, col_c in [("PLF", "PLF", "PLF_CRISE"), ("CFX", "CFX", "CFX_CRISE")]:
            annual_normal = r[col_n]
            annual_crisis = r[col_c]
            if pd.isna(annual_normal):
                continue
            for m in range(1, 13):
                rows.append({
                    "year": int(r["ANNEE"]),
                    "month": m,
                    "site_code": site,
                    "indicateur": r["INDICATEUR"],
                    "sous_indicateur": r["SOUS-INDICATEUR"],
                    "unite": r["UNITE"],
                    "value": round(annual_normal * month_pct_normal[m] / 100, 2),
                    "value_crise": round(annual_crisis * month_pct_crisis[m] / 100, 2),
                })
    return pd.DataFrame(rows)
