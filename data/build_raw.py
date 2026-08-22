# build_raw.py — écrit les CSV bruts annuels (un par domaine), extraits à la main des 3 PDF
# fournis (SLP-CHF2012, SLP-CHX2015, SLP-CHF2016).
# Schéma commun : ANNEE, INDICATEUR, SOUS-INDICATEUR, PLF, CFX, TOTAL, UNITE
#
# NB: quand seule la valeur "groupe" (PSL+CFX) est publiée dans le rapport, PLF/CFX
# sont laissés vides ; l'étape d'interpolation (interpolate.py) les répartira.

import csv
import os

HEADERS = ["ANNEE", "INDICATEUR", "SOUS-INDICATEUR", "PLF", "CFX", "TOTAL", "UNITE"]


def write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        for r in rows:
            w.writerow(r)
    print(f"✅ {path} ({len(rows)} lignes)")


# ============================================================
# ACTIVITÉ & SERVICE
# ============================================================
activity_rows = [
    # ANNEE, INDICATEUR, SOUS-INDICATEUR, PLF, CFX, TOTAL, UNITE
    (2011, "Urgences", "Passages totaux", 83002, "", "", "passages"),
    (2012, "Urgences", "Passages totaux", 85993, "", "", "passages"),
    (2015, "Urgences", "Passages totaux", "", "", 121721, "passages"),
    (2016, "Urgences", "Passages totaux", "", "", 127678, "passages"),

    (2012, "Urgences", "Patients admis en hospitalisation", 10063, "", "", "patients"),
    (2015, "Urgences", "Patients admis en hospitalisation", "", "", 7588, "patients"),

    (2012, "Consultations", "Consultations externes", 657047, 3911, 660958, "consultations"),
    (2015, "Consultations", "Consultations externes", "", "", 607950, "consultations"),
    (2016, "Consultations", "Consultations externes", "", "", 644602, "consultations"),

    (2012, "Séjours", "Hospitalisation complète (>24h)", 64693, 3494, 68187, "séjours"),
    (2015, "Séjours", "Hospitalisation complète (>24h)", 68533, 4689, 73222, "séjours"),
    (2016, "Séjours", "Hospitalisation complète (>24h)", "", "", 75079, "séjours"),

    (2012, "Séjours", "Ambulatoire (<24h)", 86529, 1184, 87713, "séjours"),
    (2015, "Séjours", "Ambulatoire (<24h)", 93558, 1614, 95172, "séjours"),
    (2016, "Séjours", "Ambulatoire (<24h)", "", "", 100319, "séjours"),

    (2015, "Actes", "Actes opératoires", "", "", 47925, "actes"),
    (2015, "Naissances", "Accouchements", "", "", 2279, "naissances"),
    (2012, "Naissances", "Naissances", "", "", 2457, "naissances"),
    (2016, "Naissances", "Accouchements", "", "", 2186, "naissances"),
    (2012, "Greffes", "Transplantations", "", "", 314, "greffes"),
    (2015, "Greffes", "Transplantations", "", "", 378, "greffes"),
    (2016, "Greffes", "Transplantations", "", "", 394, "greffes"),
]
write_csv("activity_service/activity_service-data.csv", activity_rows)

# ============================================================
# PATIENTS — causes d'hospitalisation (en nombre de séjours)
# ============================================================
patients_rows = [
    (2012, "Causes d'hospitalisation", "Pathologies cancéreuses", "", "", 46789, "séjours"),
    (2012, "Causes d'hospitalisation", "Pathologies neurologiques", "", "", 25843, "séjours"),
    (2012, "Causes d'hospitalisation", "Pathologies cardio-vasculaires", "", "", 15275, "séjours"),
    (2012, "Causes d'hospitalisation", "Pathologies endocriniennes / métaboliques / nutrition", "", "", 11611, "séjours"),
    (2012, "Causes d'hospitalisation", "Pathologies de l'appareil génito-urinaire", "", "", 11966, "séjours"),
    (2012, "Causes d'hospitalisation", "Pathologies orthopédiques et traumatologiques", "", "", 10064, "séjours"),
    (2012, "Causes d'hospitalisation", "Pathologies de l'appareil digestif", "", "", 6286, "séjours"),
    (2012, "Causes d'hospitalisation", "Obstétrique", "", "", 4548, "séjours"),
    (2012, "Causes d'hospitalisation", "Pathologies infectieuses", "", "", 3545, "séjours"),

    (2015, "Causes d'hospitalisation", "Pathologies cancéreuses", "", "", 59017, "séjours"),
    (2015, "Causes d'hospitalisation", "Pathologies neurologiques", "", "", 27748, "séjours"),
    (2015, "Causes d'hospitalisation", "Pathologies cardio-vasculaires", "", "", 15938, "séjours"),
    (2015, "Causes d'hospitalisation", "Pathologies endocriniennes / métaboliques / nutrition", "", "", 12552, "séjours"),
    (2015, "Causes d'hospitalisation", "Pathologies de l'appareil génito-urinaire", "", "", 12154, "séjours"),
    (2015, "Causes d'hospitalisation", "Pathologies orthopédiques et traumatologiques", "", "", 10850, "séjours"),
    (2015, "Causes d'hospitalisation", "Pathologies de l'appareil digestif", "", "", 8566, "séjours"),
    (2015, "Causes d'hospitalisation", "Obstétrique", "", "", 4361, "séjours"),
    (2015, "Causes d'hospitalisation", "Pathologies infectieuses", "", "", 3552, "séjours"),
]
write_csv("patients/patients-data.csv", patients_rows)

# ============================================================
# CAPACITÉ — lits
# ============================================================
capacity_rows = [
    (2012, "Lits", "Lits totaux (toutes disciplines)", 1647, 485, 2132, "lits"),
    (2015, "Lits", "Lits totaux (toutes disciplines)", 1742, 474, 2216, "lits"),
    (2016, "Lits", "Lits totaux (toutes disciplines)", "", "", 2229, "lits"),

    (2015, "Lits", "MCO", "", "", 1618, "lits"),
    (2015, "Lits", "SSR", "", "", 275, "lits"),
    (2015, "Lits", "SLD", "", "", 189, "lits"),
    (2015, "Lits", "Psychiatrie", "", "", 134, "lits"),

    (2012, "Lits", "MCO", "", "", 1510, "lits"),
    (2012, "Lits", "SSR", "", "", 209, "lits"),
    (2012, "Lits", "SLD", "", "", 248, "lits"),
    (2012, "Lits", "Psychiatrie", "", "", 140, "lits"),
]
write_csv("capacity/capacity-data.csv", capacity_rows)

# ============================================================
# FINANCE
# ============================================================
finance_rows = [
    (2012, "Budget", "Dépenses d'exploitation", 698.81, 67.27, 766.08, "M€"),
    (2015, "Budget", "Dépenses d'exploitation", 807.13, 68.56, 875.69, "M€"),
    (2016, "Budget", "Dépenses d'exploitation", "", "", 887.3, "M€"),

    (2012, "Budget", "Recettes", 711.52, 55.66, 767.18, "M€"),
    (2015, "Budget", "Recettes", 839.66, 58.91, 898.57, "M€"),
]
write_csv("finance/finance-data.csv", finance_rows)

# ============================================================
# RH — effectifs
# ============================================================
hr_rows = [
    (2012, "Effectifs", "Médecins (ETP)", 1160, 93, 1253, "ETP"),
    (2015, "Effectifs", "Médecins (ETP)", 1506, 115, 1621, "ETP"),
    (2016, "Effectifs", "Médecins (ETP)", "", "", 947, "ETP"),

    (2012, "Effectifs", "Médecins (effectif physique)", 1846, 138, 1984, "personnes"),
    (2016, "Effectifs", "Médecins (effectif physique)", "", "", 2778, "personnes"),

    (2012, "Effectifs", "Personnel paramédical (ETP)", 6312, 770, 7082, "ETP"),
    (2015, "Effectifs", "Personnel paramédical (ETP)", 6897, 953, 7850, "ETP"),
    (2016, "Effectifs", "Personnel paramédical (ETP)", "", "", 6585, "ETP"),
]
write_csv("hr/hr-data.csv", hr_rows)

# ============================================================
# LOGISTIQUE
# ============================================================
logistics_rows = [
    (2012, "Restauration", "Nombre de repas", 3238399, 1273338, 4511737, "repas"),
    (2015, "Restauration", "Nombre de repas", 1999447, 1221924, 3224371, "repas"),

    (2012, "Déchets", "DASRIA (déchets à risque infectieux)", 1086.19, 48, 1134.19, "tonnes"),
    (2015, "Déchets", "DASRIA (déchets à risque infectieux)", 1070, 53, 1123, "tonnes"),

    (2012, "Déchets", "DAOM / DMA (déchets ménagers assimilés)", 2776.78, 672, 3448.78, "tonnes"),
    (2015, "Déchets", "DAOM / DMA (déchets ménagers assimilés)", 2930, 690, 3620, "tonnes"),
]
write_csv("logistics/logistics-data.csv", logistics_rows)

print("\nToutes les données brutes ont été générées.")
