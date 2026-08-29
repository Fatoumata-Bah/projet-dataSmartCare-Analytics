from pages._common import render_annual_page

NOTES = {
    "Effectifs": (
        "⚠️ Depuis 2016, les internes et étudiants en médecine sont comptés à part "
        "des médecins (avant, ils étaient inclus dans le total) : la forte baisse "
        "affichée pour les médecins en 2016 reflète surtout ce changement de "
        "méthode de comptage, pas une vraie perte de personnel."
    ),
}


def render(st_module):
    render_annual_page(
        st_module, "data/hr/hr-all.csv",
        key_prefix="hr", indicateur_notes=NOTES,
    )
