# pages/_common.py — widgets de filtre et helpers de graphique partagés

import pandas as pd
import altair as alt  # noqa: F401 (used by chart builders below)

COULEUR_PREVISION = "#E67E22"
PALETTE_ANNEES = ["#003A8F", "#0B5ED7", "#1F77B4", "#4A90E2", "#6BAED6", "#9ECAE1", "#2CA02C"]


def site_filter(st_module, df, key_prefix=""):
    hospital_choice = st_module.sidebar.radio(
        "Site / Total",
        options=["TOTAL", "PLF", "CFX"],
        format_func=lambda x: {"TOTAL": "Total (PSL + CFX)", "PLF": "Pitié-Salpêtrière (PSL)", "CFX": "Charles Foix (CFX)"}[x],
        key=f"{key_prefix}_site",
    )
    if hospital_choice in ("PLF", "CFX"):
        return df[df["site_code"] == hospital_choice]
    return df  # TOTAL -> on garde PLF + CFX (agrégé ensuite par les groupby)


def mode_filter(st_module, key_prefix=""):
    mode_choice = st_module.sidebar.radio(
        "Mode",
        options=["Normal", "Crise"],
        index=0,
        format_func=lambda x: {"Normal": "Situation normale", "Crise": "Crise sanitaire (simulation)"}[x],
        key=f"{key_prefix}_mode",
    )
    return mode_choice, ("value" if mode_choice == "Normal" else "value_crise")


def granularity_filter(st_module, key_prefix=""):
    return st_module.sidebar.radio(
        "Granularité temporelle",
        options=["Mensuel", "Trimestriel", "Annuel"],
        index=0,
        key=f"{key_prefix}_gran",
    )


def apply_granularity(df, value_col, granularity):
    """df doit avoir les colonnes year, month. Retourne un df avec une colonne
    'periode' (int, 1..12 / 1..4 / année) et 'value' agrégée."""
    d = df.copy()
    if granularity == "Mensuel":
        d["periode"] = d["month"]
        agg = d.groupby(["year", "periode"])[value_col].sum().reset_index()
        agg = agg.rename(columns={value_col: "value"})
        agg["periode_label"] = agg["periode"].astype(int)
        x_title = "Mois"
    elif granularity == "Trimestriel":
        d["periode"] = ((d["month"] - 1) // 3 + 1).astype(int)
        agg = d.groupby(["year", "periode"])[value_col].sum().reset_index()
        agg = agg.rename(columns={value_col: "value"})
        agg["periode_label"] = "T" + agg["periode"].astype(str)
        x_title = "Trimestre"
    else:  # Annuel
        agg = d.groupby(["year"])[value_col].sum().reset_index()
        agg = agg.rename(columns={value_col: "value"})
        agg["periode"] = 1
        agg["periode_label"] = agg["year"].astype(str)
        x_title = "Année"
    return agg, x_title


def line_chart_multi_year(agg, x_title, years_all, forecast_year=None):
    color_range = [COULEUR_PREVISION if y == forecast_year else PALETTE_ANNEES[i % len(PALETTE_ANNEES)]
                   for i, y in enumerate(years_all)]
    return (
        alt.Chart(agg)
        .mark_line(point=True)
        .encode(
            x=alt.X("periode:O", title=x_title),
            y=alt.Y("value:Q", title="Volume", axis=alt.Axis(format=",.0f")),
            color=alt.Color("year:O", title="Année", scale=alt.Scale(domain=years_all, range=color_range)),
            tooltip=["year", "periode_label", alt.Tooltip("value:Q", format=",.1f")],
        )
        .properties(height=340)
    )


def bar_chart_annual(agg):
    return (
        alt.Chart(agg)
        .mark_bar()
        .encode(
            x=alt.X("year:O", title="Année"),
            y=alt.Y("value:Q", title="Valeur", axis=alt.Axis(format=",.0f")),
            tooltip=["year", alt.Tooltip("value:Q", format=",.1f")],
        )
        .properties(height=340)
    )


def render_monthly_page(st_module, data_path, key_prefix):
    """Page générique pour un domaine avec données mensuelles reconstituées
    (indicateur / sous_indicateur / year / month / value / value_crise)."""
    from utils import load_data, forecast_next_year

    df = load_data(data_path)

    st_module.sidebar.header("Filtres")
    mode_choice, value_col = mode_filter(st_module, key_prefix)
    dff = site_filter(st_module, df, key_prefix)
    granularity = granularity_filter(st_module, key_prefix)
    show_forecast = st_module.sidebar.checkbox(
        "Afficher prévision (SARIMA, année suivante)", value=False, key=f"{key_prefix}_fc"
    )

    years_hist = sorted(dff["year"].unique().tolist())
    year_options = ["Toutes"] + years_hist
    year_choice = st_module.sidebar.selectbox("Année", options=year_options, key=f"{key_prefix}_year")

    st_module.caption(f"Mode affiché : **{mode_choice}**  |  Granularité : **{granularity}**")

    indicateurs = sorted(dff["indicateur"].dropna().unique().tolist())
    tabs = st_module.tabs(indicateurs)

    for tab, indic in zip(tabs, indicateurs):
        with tab:
            st_module.subheader(indic)
            df_indic = dff[dff["indicateur"] == indic]
            sous_list = sorted(df_indic["sous_indicateur"].dropna().unique().tolist())

            for sous in sous_list:
                df_s = df_indic[df_indic["sous_indicateur"] == sous]
                unite = df_s["unite"].iloc[0] if len(df_s) else ""

                df_plot = df_s if year_choice == "Toutes" else df_s[df_s["year"] == year_choice]
                years_all = years_hist

                forecast_year = None
                if show_forecast:
                    fc_input = df_s[["year", "month", value_col]].rename(columns={value_col: "value"})
                    fc = forecast_next_year(fc_input)
                    if not fc.empty:
                        forecast_year = int(fc["year"].iloc[0])
                        fc_full = fc.assign(indicateur=indic, sous_indicateur=sous, unite=unite, site_code="PREVISION")
                        fc_full[value_col] = fc_full["value"]
                        df_plot = pd.concat([df_plot, fc_full], ignore_index=True)
                        years_all = years_hist + [forecast_year]

                agg, x_title = apply_granularity(df_plot, value_col, granularity)

                if granularity == "Annuel":
                    chart = bar_chart_annual(agg)
                else:
                    chart = line_chart_multi_year(agg, x_title, sorted(set(years_all)), forecast_year)

                subtitle = f"{sous} ({unite}) — {mode_choice}"
                if forecast_year:
                    subtitle += f" — prévision {forecast_year} en orange"
                chart = chart.properties(title={"text": indic, "subtitle": subtitle})
                st_module.altair_chart(chart, width='stretch')
                st_module.markdown("<div style='margin-bottom:2rem;'></div>", unsafe_allow_html=True)

            with st_module.expander("Voir le détail (tableau annuel)"):
                table = (
                    df_indic.groupby(["year", "unite", "sous_indicateur"])[value_col]
                    .sum().reset_index()
                    .rename(columns={"year": "Année", "unite": "Unité", "sous_indicateur": "Sous-indicateur", value_col: "Valeur"})
                )
                st_module.dataframe(table.sort_values(["Sous-indicateur", "Année"]), width='stretch')


def render_annual_page(st_module, data_path, key_prefix):
    """Page générique pour un domaine sans reconstruction mensuelle
    (indicateur / sous_indicateur / year / value / value_crise)."""
    from utils import load_data

    df = load_data(data_path)

    st_module.sidebar.header("Filtres")
    mode_choice, value_col = mode_filter(st_module, key_prefix)
    dff = site_filter(st_module, df, key_prefix)

    st_module.caption(f"Mode affiché : **{mode_choice}**  |  Données annuelles (pas de saisonnalité simulée pour ce domaine)")

    indicateurs = sorted(dff["indicateur"].dropna().unique().tolist())
    tabs = st_module.tabs(indicateurs)

    for tab, indic in zip(tabs, indicateurs):
        with tab:
            st_module.subheader(indic)
            df_indic = dff[dff["indicateur"] == indic]
            sous_list = sorted(df_indic["sous_indicateur"].dropna().unique().tolist())

            for sous in sous_list:
                df_s = df_indic[df_indic["sous_indicateur"] == sous]
                unite = df_s["unite"].iloc[0] if len(df_s) else ""
                agg = df_s.groupby("year")[value_col].sum().reset_index().rename(columns={value_col: "value"})
                chart = bar_chart_annual(agg).properties(
                    title={"text": indic, "subtitle": f"{sous} ({unite}) — {mode_choice}"}
                )
                st_module.altair_chart(chart, width='stretch')
                st_module.markdown("<div style='margin-bottom:2rem;'></div>", unsafe_allow_html=True)

            with st_module.expander("Voir le détail (tableau)"):
                table = (
                    df_indic.groupby(["year", "unite", "sous_indicateur"])[value_col]
                    .sum().reset_index()
                    .rename(columns={"year": "Année", "unite": "Unité", "sous_indicateur": "Sous-indicateur", value_col: "Valeur"})
                )
                st_module.dataframe(table.sort_values(["Sous-indicateur", "Année"]), width='stretch')
