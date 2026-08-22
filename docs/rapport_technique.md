# Rapport technique — PSL-CFX

> Livrable 1/2 (cf. énoncé) : sources des données, traitements, choix et
> justification des modèles. Squelette à compléter — voir aussi `README.md`
> à la racine pour le détail des hypothèses déjà documentées dans le code.

## 1. Sources des données

- Rapports "Chiffres Clés" annuels des Hôpitaux Universitaires Pitié-Salpêtrière —
  Charles Foix (AP-HP), disponibles dans `sources/` :
  - `SLP-CHF2012.pdf` — Chiffres Clés 2012
  - `SLP-CHX2015.pdf` — Chiffres Clés 2015
  - `SLP-CHF2016.pdf` — Chiffres Clés 2016
- Limite : uniquement 3 années disponibles, sous forme d'agrégats **annuels**
  (aucune donnée mensuelle/journalière dans les rapports sources).

## 2. Extraction et structuration du dataset

- Schéma commun retenu : `ANNEE, INDICATEUR, SOUS-INDICATEUR, PLF, CFX, TOTAL, UNITE`
  (`data/<domaine>/<domaine>-data.csv`, générés par `data/build_raw.py`).
- 6 domaines couverts : Activité & Service, Patients (pathologies), Capacité (lits),
  Finances, RH, Logistique.
- Domaine Qualité (indicateurs IPAQSS) volontairement exclu du dataset dynamique —
  voir §4.3.

_TODO : détailler ici, pour chaque domaine, les indicateurs retenus et la page/le
tableau source du PDF dont ils sont extraits (traçabilité)._

## 3. Traitements appliqués

### 3.1 Interpolation inter-annuelle
`data/pipeline.py::interpolate_annual` — comble les années manquantes (2011,
2013, 2014, 2017) par interpolation linéaire entre les points connus (2012,
2015, 2016), avec extrapolation aux bornes. Reconstruction croisée PLF/CFX/TOTAL
quand une seule des trois valeurs est publiée.

_TODO : discuter la limite de l'interpolation linéaire (pas de logique métier,
juste une droite entre deux points connus) et les alternatives envisagées._

### 3.2 Simulation de crise sanitaire
`data/pipeline.py::apply_crisis` — coefficient multiplicatif unique par domaine :

| Domaine | Coefficient | Justification (à sourcer) |
|---|---|---|
| Activité & Service | ×1,6 | Hypothèse : +60% d'activité (urgences/séjours/consultations) |
| Patients | ×1,8 | Hypothèse : +80% de séjours (charge de morbidité accrue) |
| Capacité | ×1,15 | Hypothèse : +15% de lits ouverts en renfort |
| Finances | ×1,30 | Hypothèse : +30% de dépenses (surcoûts personnel/EPI) |
| RH | ×1,10 | Hypothèse : +10% d'effectifs mobilisés |
| Logistique | ×1,25 | Hypothèse : +25% de consommation (déchets à risque, EPI) |

_TODO : remplacer ces coefficients "au jugé" par des ordres de grandeur sourcés
(ex. retour d'expérience AP-HP attentats du 13 novembre 2015, vagues COVID)._

### 3.3 Reconstitution de la saisonnalité mensuelle
`data/pipeline.py::reconstruct_monthly` — profil de répartition mensuelle en %
assumé (mode normal : légère sur-activité hiver/été ; mode crise : profil "vague
épidémique"), appliqué uniquement aux domaines Activité & Service et Patients,
où une saisonnalité médicale a du sens.

_TODO : justifier les % choisis (grippe hivernale, canicule estivale...) avec
des sources externes (Santé Publique France, littérature épidémiologique)._

## 4. Choix et justification des modèles

### 4.1 Modèle prédictif : SARIMA
`utils.py::forecast_next_year` — `SARIMAX(order=(1,1,1), seasonal_order=(1,1,1,12))`
sur la série mensuelle reconstituée. Nécessite ≥ 24 points mensuels.

_TODO : expliquer le choix des ordres (p,d,q)(P,D,Q,s), présenter les résidus /
diagnostics du modèle, discuter la fiabilité étant donné que la série d'entrée
est elle-même une reconstruction (pas des données observées)._

### 4.2 Simulation de crise : approche multiplicative
Choix d'un coefficient unique par domaine plutôt qu'un modèle plus fin (ex. courbe
épidémique SIR) — à justifier par la simplicité et la lisibilité pour un public
non technique (cf. contrainte "pas de jargon mathématique" de l'infographie).

### 4.3 Exclusion du domaine Qualité
Les indicateurs IPAQSS sont des taux de traçabilité en %, plafonnés à 100.
Un coefficient multiplicatif (utilisé pour les volumes) ferait mécaniquement
dépasser 100% pour toute valeur de départ > 100/coefficient — non pertinent.
Une approche additive plafonnée (`min(100, valeur + delta)`) serait nécessaire
si ce domaine doit être intégré ultérieurement.

## 5. Limites générales et pistes d'amélioration

- Seulement 3 années sources → interpolation/extrapolation fragiles.
- Saisonnalité et crise = hypothèses, pas des données mesurées.
- _TODO : compléter avec les retours de la relecture / soutenance._
