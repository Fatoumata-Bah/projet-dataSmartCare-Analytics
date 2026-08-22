# utils.py — fonctions partagées : chargement des CSV, prévision SARIMA
import pandas as pd
import streamlit as st


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data
def forecast_next_year(df: pd.DataFrame) -> pd.DataFrame:
    """Prévision SARIMA (saisonnalité mensuelle, période 12) de l'année suivante,
    à partir d'une série mensuelle agrégée tous sites confondus (colonnes year, month, value).
    Nécessite au moins 24 points mensuels (2 ans) pour être significatif.
    """
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    ts = (
        df.groupby(["year", "month"])["value"].sum().reset_index()
        .sort_values(["year", "month"])
    )
    if len(ts) < 24:
        return pd.DataFrame()

    ts["date"] = pd.to_datetime(ts["year"].astype(str) + "-" + ts["month"].astype(str) + "-01")
    series = ts.set_index("date")["value"].asfreq("MS").interpolate()

    try:
        model = SARIMAX(
            series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
            enforce_stationarity=False, enforce_invertibility=False,
        )
        results = model.fit(disp=False)
        pred = results.get_forecast(steps=12).predicted_mean
        last_year = int(series.index[-1].year)
        return pd.DataFrame({"year": last_year + 1, "month": range(1, 13), "value": pred.values})
    except Exception:
        return pd.DataFrame()
