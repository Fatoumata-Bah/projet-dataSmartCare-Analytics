# PSL-CFX Analytics

Projet Data Epitech sur les Hôpitaux Universitaires Pitié-Salpêtrière —
Charles Foix (PSL-CFX). À partir des 3 rapports "Chiffres Clés" fournis par
l'établissement (2012, 2015, 2016), j'ai construit un dataset structuré, une
simulation de crise sanitaire, une reconstitution de la saisonnalité
mensuelle, une prévision SARIMA, et une infographie interactive avec
Streamlit pour restituer tout ça de façon compréhensible.

## Rapports

- 📄 [Rapport technique](docs/rapport_technique.md) - sources des données,
  traitements appliqués, choix et justification des modèles.
- 📄 [Rapport de mise en place](docs/rapport_mise_en_place.md) -
  propositions pour gérer les afflux de patients et se préparer aux crises
  sanitaires.

## Structure du repo

```
.
├── app.py                     # Point d'entrée du dashboard Streamlit
├── utils.py                   # Chargement des données + prévision SARIMA
├── pages/                     # Une page par domaine du dashboard
├── data/
│   ├── build_raw.py           # Écrit les CSV bruts annuels (extraits des PDF)
│   ├── pipeline.py            # Interpolation, simulation crise, saisonnalité
│   ├── generate_all.py        # Applique le pipeline à chaque domaine
│   └── <domaine>/              # CSV générés par domaine (bruts + interpolés + finaux)
├── sources/                   # PDF sources fournis par l'école (rapports annuels)
├── exports/                   # Export Excel consolidé (dataset_PSL_CFX.xlsx)
├── docs/                      # Rapports + figures du modèle de prévision
├── tests/                     # Tests (rendu des pages sans exception)
└── .vscode/                   # Config VS Code (lancer le dashboard en F5)
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer le dashboard

```bash
streamlit run app.py
```

Ça ouvre automatiquement le navigateur sur **<http://localhost:8501>**. Ou
depuis VS Code : `F5` → configuration **"Streamlit: Dashboard"** (déjà
configurée dans `.vscode/launch.json`).

## Régénérer les données

Si je modifie `data/build_raw.py` (ajout d'indicateurs, correction de
valeurs), je régénère le pipeline complet :

```bash
cd data
python3 build_raw.py
python3 generate_all.py
```

> Sous Windows, si la console affiche une `UnicodeEncodeError` sur les
> caractères `✅`, lancer plutôt `set PYTHONIOENCODING=utf-8` (ou
> `$env:PYTHONIOENCODING="utf-8"` en PowerShell) avant ces deux commandes.

### Export Excel (`exports/dataset_PSL_CFX.xlsx`)

Ce fichier est **maintenu manuellement** (résumé mis en forme, pas un export
brut des CSV) : `data/generate_all.py` ne le régénère pas automatiquement. Si
je modifie `data/build_raw.py`, je pense à mettre à jour ce fichier à la main
à partir des CSV `*-interpolated.csv` / `*-all.csv` correspondants.

### Visuels du modèle de prévision

```bash
python docs/generate_figures.py
```

Régénère les figures du dossier `docs/figures/` (courbe de prévision +
intervalle de confiance, diagnostics du modèle) à partir de la même fonction
que le dashboard (`utils.py::fit_forecast_model`).

## Tests

```bash
python3 tests/test_app.py
# ou, avec pytest :
pytest tests/
```

Vérifie que chaque page du dashboard se rend sans exception, en mode Normal et
en mode Crise.

## Domaines couverts

| Domaine | Saisonnalité mensuelle | Coefficient de crise |
| --- | --- | --- |
| Urgences & Activité | ✅ simulée | ×1,6 |
| Patients / Pathologies | ✅ simulée | ×1,8 |
| Capacité (lits) | ❌ annuel seul | ×1,15 |
| Finances | ❌ annuel seul | ×1,30 |
| RH | ❌ annuel seul | ×1,10 |
| Logistique | ❌ annuel seul | ×1,25 |
| Qualité (IPAQSS) | — **exclu** | voir `docs/rapport_technique.md` §4.3 |

## ⚠️ Limite méthodologique à retenir

Les 3 rapports sources ne fournissent que des **totaux annuels**. Toute
décomposition mensuelle, tout coefficient de crise sanitaire, est donc une
**hypothèse de modélisation explicite** documentée dans le code
(`data/pipeline.py`) et justifiée dans le
[rapport technique](docs/rapport_technique.md) — pas une donnée mesurée. Je
l'assume et le documente plutôt que de le cacher : deux ruptures de méthode
entre les rapports sources (comptage des urgences, effectifs médicaux 2016)
ne peuvent pas être réconciliées avec les 3 PDF disponibles, et sont
signalées directement dans le dashboard.
