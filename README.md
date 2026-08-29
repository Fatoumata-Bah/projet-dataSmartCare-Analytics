# PSL-CFX Analytics

Projet Data Epitech — Hôpitaux Universitaires Pitié-Salpêtrière — Charles Foix (PSL-CFX).

Construit à partir des 3 rapports "Chiffres Clés" fournis (2012, 2015, 2016) :
dataset structuré, simulation de crise sanitaire, saisonnalité mensuelle,
prévision SARIMA et infographie interactive (Streamlit).

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
├── docs/                      # Rapport technique + rapport de mise en place (à compléter)
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

Ou depuis VS Code : `F5` → configuration **"Streamlit: Dashboard"** (déjà
configurée dans `.vscode/launch.json`).

## Régénérer les données

Si vous modifiez `data/build_raw.py` (ajout d'indicateurs, correction de
valeurs), régénérez le pipeline complet :

```bash
cd data
python3 build_raw.py
python3 generate_all.py
```

> Sous Windows, si la console affiche une `UnicodeEncodeError` sur les
> caractères `✅`, lancez plutôt `set PYTHONIOENCODING=utf-8` (ou
> `$env:PYTHONIOENCODING="utf-8"` en PowerShell) avant ces deux commandes.

### Export Excel (`exports/dataset_PSL_CFX.xlsx`)

Ce fichier est **maintenu manuellement** (résumé mis en forme, pas un export
brut des CSV) : `data/generate_all.py` ne le régénère pas automatiquement.
Si vous modifiez `data/build_raw.py`, pensez à mettre à jour ce fichier à la
main à partir des CSV `*-interpolated.csv` / `*-all.csv` correspondants.

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
|---|---|---|
| Urgences & Activité | ✅ simulée | ×1,6 |
| Patients / Pathologies | ✅ simulée | ×1,8 |
| Capacité (lits) | ❌ annuel seul | ×1,15 |
| Finances | ❌ annuel seul | ×1,30 |
| RH | ❌ annuel seul | ×1,10 |
| Logistique | ❌ annuel seul | ×1,25 |
| Qualité (IPAQSS) | — **exclu** (indicateurs en %, voir `docs/rapport_technique.md` §4.3) |

## ⚠️ Limite méthodologique à retenir

Les 3 rapports sources ne fournissent que des **totaux annuels**. Toute
décomposition mensuelle, tout coefficient de crise sanitaire, est donc une
**hypothèse de modélisation explicite** documentée dans le code
(`data/pipeline.py`) et à justifier dans `docs/rapport_technique.md` — pas une
donnée mesurée.

## Livrables du projet (cf. énoncé, `sources/Projet_Data_Ko.pdf`)

- [x] Dataset structuré (`data/`, export `exports/dataset_PSL_CFX.xlsx` — à
      rafraîchir manuellement, voir note ci-dessus)
- [x] Modèle de prévision SARIMA (`utils.py`)
- [x] Simulation de crise sanitaire (`data/pipeline.py`, coefficients sourcés
      dans `docs/rapport_technique.md` §3.2)
- [x] Infographie interactive (`app.py` + `pages/`)
- [x] Rapport technique (`docs/rapport_technique.md`)
- [x] Rapport de mise en place (`docs/rapport_mise_en_place.md`)
- [ ] Présentation de soutenance
