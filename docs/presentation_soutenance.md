# Plan de soutenance — PSL-CFX Analytics

> Trame de contenu (pas de mise en forme) pour préparer les slides. À adapter
> au temps réellement imparti. S'appuie sur `docs/rapport_technique.md` et
> `docs/rapport_mise_en_place.md` — ne les recopie pas, les résume.
>
> Rappel de l'énoncé (`sources/Projet_Data_Ko.pdf` p.6-7) : la soutenance doit
> couvrir 4 points précis — (1) démonstration complète du prototype et des
> simulations, (2) explication des choix techniques et analytiques,
> (3) analyse des résultats du modèle prédictif et recommandations
> concrètes, (4) discussion sur les perspectives d'évolution. Le plan
> ci-dessous suit cet ordre.

## Minutage indicatif (à ajuster selon le temps réel imparti)

| Bloc | Durée |
|---|---|
| 1. Contexte & objectifs | 1-2 min |
| 2. Démonstration du dashboard (live) | 5-6 min |
| 3. Choix techniques et analytiques | 3-4 min |
| 4. Résultats du modèle prédictif + recommandations | 4-5 min |
| 5. Limites et perspectives | 2 min |
| Questions | reste du temps |

---

## Slide 1 — Titre

PSL-CFX Analytics — Infographie interactive, prévision et simulation de
crise sanitaire pour les Hôpitaux Universitaires Pitié-Salpêtrière —
Charles Foix.

## Slide 2 — Contexte (1-2 min)

- Hôpital confronté à des pics d'activité saisonniers, une saturation des
  urgences, un manque de personnel et des risques de rupture de stock en
  situation de crise (cf. énoncé).
- Objectif du projet : construire un dataset structuré à partir des seuls
  documents disponibles (3 rapports "Chiffres Clés" 2012/2015/2016), en tirer
  une prévision d'activité et une simulation de crise sanitaire, le tout
  restitué dans une infographie compréhensible **sans jargon technique**.
- **Point à assumer dès le début** : les rapports sources ne donnent que des
  totaux annuels — tout le reste (mois, crise) est une hypothèse de
  modélisation explicite, pas une mesure. C'est le fil rouge de toute la
  présentation.

## Slide 3-8 — Démonstration du dashboard (5-6 min, LIVE)

Ne pas dérouler toutes les pages en détail — choisir un parcours qui
prouve les 4 exigences de l'énoncé (bascule Normal/Crise, filtres de dates,
UX soignée, jargon médical acceptable / pas de jargon math).

**Parcours suggéré** (`streamlit run app.py`) :
1. **Vue d'ensemble** — indicateurs clés, mode Normal. Montre l'état actuel
   de PSL-CFX (capacité, urgences, effectifs) demandé par l'énoncé.
2. **Urgences & Activité**, mode Normal, granularité Mensuelle — montrer le
   pic hivernal (déc-jan-fév). Pointer l'avertissement affiché sur cet
   onglet (rupture de méthode de comptage 2015/2016) : **c'est une preuve de
   rigueur à mettre en avant, pas à cacher**.
3. Basculer en mode **Crise** sur la même page — le profil change de forme
   (pic au printemps, rebond en novembre) et le volume grimpe. Expliquer en
   une phrase simple : "on modélise une vague épidémique, pas juste un +X%
   uniforme dans le temps".
4. Cocher "Afficher une estimation pour l'année suivante" — montrer la
   courbe de prévision qui se prolonge.
5. **RH** — montrer l'avertissement sur "Effectifs" (rupture de comptage
   internes/étudiants 2016) : même logique de transparence.
6. Filtre **Site** (PSL / CFX / Total) et **granularité** (mensuel /
   trimestriel / annuel) sur une page au choix — cocher explicitement les
   exigences "filtres de dates" de l'énoncé.

## Slide 9 — Choix techniques et analytiques (3-4 min)

- **Extraction et structuration** : schéma commun `ANNEE / INDICATEUR /
  SOUS-INDICATEUR / PLF / CFX / TOTAL / UNITE`, 6 domaines couverts, domaine
  Qualité volontairement exclu (taux plafonnés à 100%, incompatibles avec un
  coefficient multiplicatif — expliquer pourquoi en une phrase).
- **Interpolation inter-annuelle** : combler 2011/2013/2014/2017 par
  interpolation linéaire — assumer la limite (pas de logique métier, juste
  une droite entre deux points connus).
- **Saisonnalité mensuelle** : profil assumé (hiver = pic ; crise = vague
  épidémique), pas mesuré — dire clairement que c'est une hypothèse de
  modélisation documentée.
- **Simulation de crise** : un coefficient multiplicatif par domaine,
  **sourcé** sur des données réelles COVID (DREES, ATIH, Cour des comptes,
  Assemblée nationale) plutôt qu'"au jugé" — c'est le point le plus attendu
  du jury vu l'insistance de l'énoncé ("LIRE... Re-LIRE... les sources"). Un
  ou deux chiffres clés à citer de mémoire : +14,5% de lits de réanimation
  en France en 2020 (proche du +15% retenu pour la capacité), jusqu'à 250%
  de la capacité de réa nécessaire en Île-de-France au printemps 2020.
- **Modèle prédictif SARIMA** : pourquoi ce modèle (recommandé par
  l'énoncé, standard pour une saisonnalité mensuelle), et sa limite
  assumée : il apprend sur une série reconstruite, pas observée — donc sa
  valeur est démonstrative de la mécanique, pas une vraie prédiction tant
  que le dataset ne contient pas de données mensuelles réelles.

## Slide 10-11 — Résultats du modèle prédictif + recommandations (4-5 min)

- Montrer la figure `docs/figures/forecast_urgences.png` : historique +
  prévision + intervalle de confiance. Expliquer simplement ce que
  représente l'intervalle (fourchette de confiance, pas une valeur unique).
- Montrer (rapidement, sans détailler chaque panneau) la figure
  `docs/figures/forecast_diagnostics.png` — l'occasion de montrer une
  démarche rigoureuse : "on a vérifié les résidus du modèle, et on a repéré
  une anomalie qui confirme un point de méthode déjà identifié" (le saut à
  la jonction 2015-2016 dû à la reconstruction PLF/CFX des urgences).
- **Recommandations concrètes** (résumé de `rapport_mise_en_place.md`) :
  - Court terme : renfort saisonnier calé sur le pic hivernal, extension des
    filières d'aval urgences → services (déjà en place et documentées
    efficaces sur PSL-CFX même).
  - Moyen terme : diversification fournisseurs EPI, lits tampons ciblés
    soins critiques, ligne budgétaire de réserve.
  - Long terme : mécanisme de financement d'urgence pré-négocié,
    amélioration de la collecte de données (mensuelle) pour remplacer les
    hypothèses par des données mesurées.
  - Point fort à citer : le retour d'expérience réel de PSL-CFX (attentats
    du 13 novembre 2015, Plan NOVI-H) comme base de plan de mobilisation —
    plus solide qu'une hypothèse générique.

## Slide 12 — Limites et perspectives (2 min)

- Seulement 3 années sources → toute extrapolation reste fragile.
- Deux ruptures de méthode non réconciliables (Urgences, Médecins ETP) —
  documentées et affichées dans l'app plutôt que masquées.
- Coefficient "Finances" (+30%) volontairement prudent par rapport à la
  moyenne nationale réelle (~3%) — à faire évoluer selon l'usage
  (préparation au pire cas vs estimation réaliste).
- **Perspectives** : intégrer des données mensuelles réelles (SAE, ATIH,
  data.gouv.fr) si accessibles, recalibrer la saisonnalité sur des données
  observées, étendre le domaine Qualité avec une logique additive plafonnée,
  automatiser la génération de l'export Excel.

## Slide 13 — Questions

Anticiper les questions probables (à préparer à l'oral, pas à l'écrit) :
- "Pourquoi ces coefficients précis et pas d'autres ?" → renvoyer aux
  sources citées en slide 9 + rapport technique §3.2.
- "Le modèle SARIMA sert-il vraiment à quelque chose si la série est
  reconstruite ?" → assumer la limite (slide 9), insister sur la valeur
  méthodologique/démonstrative.
- "Que feriez-vous avec plus de temps/données ?" → slide 12, perspectives.
