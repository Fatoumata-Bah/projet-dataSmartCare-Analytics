# pages/vue_ensemble.py — page d'accueil : indicateurs clés + bascule Normal/Crise
from utils import load_data


def render(st_module):
    st_module.sidebar.header("Filtres")
    mode_choice = st_module.sidebar.radio(
        "Mode",
        options=["Normal", "Crise"],
        index=0,
        format_func=lambda x: {"Normal": "Situation normale", "Crise": "Crise sanitaire (simulation)"}[x],
        key="ve_mode",
    )
    value_col = "value" if mode_choice == "Normal" else "value_crise"

    st_module.caption(
        "Vue d'ensemble du groupe hospitalier PSL–CFX. "
        f"Mode affiché : **{mode_choice}**. Dernière année disponible par domaine."
    )

    df_act = load_data("data/activity_service/activity_service-all.csv")
    df_cap = load_data("data/capacity/capacity-all.csv")
    df_fin = load_data("data/finance/finance-all.csv")
    df_hr = load_data("data/hr/hr-all.csv")

    last_year_act = int(df_act["year"].max())
    last_year_cap = int(df_cap["year"].max())
    last_year_fin = int(df_fin["year"].max())
    last_year_hr = int(df_hr["year"].max())

    def total_for(df, year, indic, sous):
        m = (df["year"] == year) & (df["indicateur"] == indic) & (df["sous_indicateur"] == sous)
        return df.loc[m, value_col].sum()

    urgences = total_for(df_act, last_year_act, "Urgences", "Passages totaux")
    sejours_hc = total_for(df_act, last_year_act, "Séjours", "Hospitalisation complète (>24h)")
    consultations = total_for(df_act, last_year_act, "Consultations", "Consultations externes")
    lits = total_for(df_cap, last_year_cap, "Lits", "Lits totaux (toutes disciplines)")
    depenses = total_for(df_fin, last_year_fin, "Budget", "Dépenses d'exploitation")
    medecins = total_for(df_hr, last_year_hr, "Effectifs", "Médecins (ETP)")

    c1, c2, c3 = st_module.columns(3)
    c1.metric(f"Passages urgences ({last_year_act})", f"{urgences:,.0f}".replace(",", " "))
    c2.metric(f"Séjours hospit. complète ({last_year_act})", f"{sejours_hc:,.0f}".replace(",", " "))
    c3.metric(f"Consultations externes ({last_year_act})", f"{consultations:,.0f}".replace(",", " "))

    c4, c5, c6 = st_module.columns(3)
    c4.metric(f"Lits installés ({last_year_cap})", f"{lits:,.0f}".replace(",", " "))
    c5.metric(f"Dépenses d'exploitation ({last_year_fin})", f"{depenses:,.1f} M€")
    c6.metric(f"Médecins ETP ({last_year_hr})", f"{medecins:,.0f}".replace(",", " "))

    st_module.divider()
    st_module.markdown(
        """
        **Navigation** : utilisez le menu à gauche pour explorer chaque domaine
        (Urgences & Activité, Patients / Pathologies, Capacité, Finances), avec
        pour chacun : bascule **Normal / Crise sanitaire**, filtre par **site**
        (PSL / CFX / Total), et **granularité temporelle** (mensuel / trimestriel /
        annuel) pour les domaines où une saisonnalité a été reconstituée.

        ⚠️ Les profils mensuels et le coefficient de crise sont des **hypothèses
        de modélisation documentées** (voir rapport technique), pas des données
        mesurées : les rapports sources ne fournissent que des totaux annuels.
        """
    )
