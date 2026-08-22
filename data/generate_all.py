# generate_all.py — construit, pour chaque domaine, les fichiers finaux utilisés
# par le dashboard :
#   <domaine>-interpolated.csv : annuel, années 2011-2017 comblées
#   <domaine>-all.csv          : annuel + crise (capacity, finance)
#                                 OU mensuel + crise (activity_service, patients)
import pandas as pd
from pipeline import interpolate_annual, apply_crisis, reconstruct_monthly

# ------------------------------------------------------------------
# Domaines "mensuels" : la saisonnalité infra-annuelle a du sens
# (flux de patients / activité) -> reconstruction mensuelle assumée
# ------------------------------------------------------------------
MONTHLY_DOMAINS = {
    "activity_service": {
        "raw": "activity_service/activity_service-data.csv",
        "coef_crisis": 1.6,
        "note": "Hypothèse : +60% d'activité (urgences/séjours/consultations) en période de crise sanitaire aiguë type pandémie.",
    },
    "patients": {
        "raw": "patients/patients-data.csv",
        "coef_crisis": 1.8,
        "note": "Hypothèse : +80% de séjours liés aux pathologies en période de crise sanitaire (charge de morbidité accrue).",
    },
}

# ------------------------------------------------------------------
# Domaines "annuels" : pas de saisonnalité infra-annuelle simulée
# (les rapports ne donnent aucun indice permettant de la justifier)
# ------------------------------------------------------------------
ANNUAL_DOMAINS = {
    "capacity": {
        "raw": "capacity/capacity-data.csv",
        "coef_crisis": 1.15,
        "note": "Hypothèse : +15% de lits mobilisés/ouverts en renfort en période de crise sanitaire (lits tampons, déprogrammation).",
    },
    "finance": {
        "raw": "finance/finance-data.csv",
        "coef_crisis": 1.30,
        "note": "Hypothèse : +30% de dépenses d'exploitation en période de crise sanitaire (surcoûts personnel, équipements, EPI).",
    },
    "hr": {
        "raw": "hr/hr-data.csv",
        "coef_crisis": 1.10,
        "note": "Hypothèse : +10% d'effectifs mobilisés (renforts, réservistes sanitaires, heures supplémentaires) en période de crise sanitaire.",
    },
    "logistics": {
        "raw": "logistics/logistics-data.csv",
        "coef_crisis": 1.25,
        "note": "Hypothèse : +25% de consommation logistique (déchets à risque infectieux, équipements de protection) en période de crise sanitaire ; repas globalement stables.",
    },
}


def process_monthly(name, cfg):
    df_raw = pd.read_csv(cfg["raw"])
    df_interp = interpolate_annual(df_raw)
    df_interp.to_csv(f"{name}/{name}-interpolated.csv", index=False)

    df_crisis = apply_crisis(df_interp, coef=cfg["coef_crisis"], note=cfg["note"])
    df_crisis.to_csv(f"{name}/{name}-with-crisis.csv", index=False)

    df_monthly = reconstruct_monthly(df_crisis)
    df_monthly.to_csv(f"{name}/{name}-all.csv", index=False)
    print(f"✅ {name}: {len(df_interp)} lignes annuelles -> {len(df_monthly)} lignes mensuelles")


def process_annual(name, cfg):
    df_raw = pd.read_csv(cfg["raw"])
    df_interp = interpolate_annual(df_raw)
    df_interp.to_csv(f"{name}/{name}-interpolated.csv", index=False)

    df_crisis = apply_crisis(df_interp, coef=cfg["coef_crisis"], note=cfg["note"])
    # format long, cohérent avec les domaines mensuels (sans colonne month)
    rows = []
    for _, r in df_crisis.iterrows():
        for site, col_n, col_c in [("PLF", "PLF", "PLF_CRISE"), ("CFX", "CFX", "CFX_CRISE")]:
            if pd.isna(r[col_n]):
                continue
            rows.append({
                "year": int(r["ANNEE"]),
                "site_code": site,
                "indicateur": r["INDICATEUR"],
                "sous_indicateur": r["SOUS-INDICATEUR"],
                "unite": r["UNITE"],
                "value": r[col_n],
                "value_crise": r[col_c],
            })
    df_long = pd.DataFrame(rows)
    df_long.to_csv(f"{name}/{name}-all.csv", index=False)
    print(f"✅ {name}: {len(df_interp)} lignes annuelles -> {len(df_long)} lignes (long format)")


# ------------------------------------------------------------------
# NB : le domaine "Qualité" (indicateurs IPAQSS, en %) est volontairement
# EXCLU de ce pipeline : ce sont des taux de traçabilité plafonnés à 100%,
# un coefficient de crise multiplicatif n'a aucun sens (dépasserait 100%).
# Le traiter nécessiterait une autre logique (ex: dégradation additive
# plafonnée), à envisager séparément si besoin.
# ------------------------------------------------------------------

if __name__ == "__main__":
    for name, cfg in MONTHLY_DOMAINS.items():
        process_monthly(name, cfg)
    for name, cfg in ANNUAL_DOMAINS.items():
        process_annual(name, cfg)
    print("\nGénération terminée.")
