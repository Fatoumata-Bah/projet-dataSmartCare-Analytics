# app.py — point d'entrée : sidebar (page / filtres) commune, contenu délégué par page
import importlib
import streamlit as st

from pages import PAGE_MODULES

st.set_page_config(page_title="PSL–CFX | Infographie (Normal vs Crise)", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Sidebar : page (commune à toutes les pages)
# ---------------------------
st.sidebar.header("Navigation")
PAGES = list(PAGE_MODULES.keys())
page_choice = st.sidebar.selectbox("Page", options=PAGES, label_visibility="collapsed")

module_name = PAGE_MODULES[page_choice]
page_module = importlib.import_module(f"pages.{module_name}")

# ---------------------------
# En-tête commun
# ---------------------------
st.title(f"Infographie {page_choice} — PSL–CFX")

# ---------------------------
# Contenu : chaque page gère ses propres filtres (elle sait si elle est
# mensuelle ou annuelle) via son propre render()
# ---------------------------
page_module.render(st)
