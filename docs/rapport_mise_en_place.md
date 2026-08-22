# Rapport de mise en place — PSL-CFX

> Livrable 2/2 (cf. énoncé) : propositions pour gérer les afflux de patients,
> propositions pour se préparer aux risques de crise sanitaire. Squelette à
> compléter avec l'équipe.

## 1. Constat — ce que montrent les données

_TODO : synthétiser, à partir du dashboard (`app.py`), les pics d'activité
identifiés (saisonnalité) et l'écart Normal vs Crise simulé par domaine._

- Urgences : ...
- Pathologies dominantes : ...
- Capacité (lits) : ...
- RH : ...
- Finances : ...
- Logistique : ...

## 2. Propositions pour gérer les afflux de patients (pics saisonniers)

_TODO. Exemples de pistes à développer :_
- Renfort de personnel anticipé sur les mois identifiés comme à risque
  (voir profil de saisonnalité `DEFAULT_MONTH_PCT_NORMAL` dans `data/pipeline.py`)
- Filières d'aval urgences → services pour réduire l'engorgement (cf. rapports
  sources 2015/2016 qui mentionnent déjà ce type d'action)
- ...

## 3. Propositions pour se préparer aux risques de crise sanitaire

_TODO. Exemples de pistes à développer, en s'appuyant sur le mode "Crise" du
dashboard (coefficients par domaine) :_
- Plan de mobilisation RH (+10% simulé) : réservistes sanitaires, astreintes
- Stocks tampons de matériel/logistique (+25% simulé de déchets à risque → donc
  de consommables)
- Lits tampons / déprogrammation (+15% simulé)
- Financement d'urgence / ligne budgétaire dédiée (+30% simulé de dépenses)
- ...

## 4. Priorisation / feuille de route

_TODO : proposer un ordre de priorité (court/moyen/long terme) pour ces
recommandations, en cohérence avec le budget et les contraintes RH réelles de
l'hôpital._
