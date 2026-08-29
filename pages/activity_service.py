from pages._common import render_monthly_page

NOTES = {
    "Urgences": (
        "⚠️ La façon de compter les passages aux urgences a changé selon les années "
        "(le rapport 2015 inclut les urgences dentaires, pas les autres années) : "
        "l'évolution d'une année sur l'autre est donc à lire avec prudence."
    ),
}


def render(st_module):
    render_monthly_page(
        st_module, "data/activity_service/activity_service-all.csv",
        key_prefix="act", indicateur_notes=NOTES,
    )
