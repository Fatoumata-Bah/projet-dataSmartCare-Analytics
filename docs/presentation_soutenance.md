# Plan de soutenance — PSL-CFX Analytics

Trame de contenu pour préparer mes slides, à adapter selon le temps qui me
sera vraiment donné. Je m'appuie sur mes deux rapports sans les recopier,
juste les résumer à l'oral. L'énoncé demande de couvrir 4 points à la
soutenance : démonstration du prototype, choix techniques, résultats du
modèle prédictif + recommandations, perspectives d'évolution — je garde cet
ordre.

## Minutage indicatif

| Bloc | Durée |
| --- | --- |
| Contexte & objectifs | 1-2 min |
| Démonstration du dashboard (live) | 5-6 min |
| Choix techniques et analytiques | 3-4 min |
| Résultats du modèle prédictif + recommandations | 4-5 min |
| Limites et perspectives | 2 min |
| Questions | reste du temps |

---

## Slide 1 — Titre

PSL-CFX Analytics — Infographie interactive, prévision et simulation de
crise sanitaire pour les Hôpitaux Universitaires Pitié-Salpêtrière —
Charles Foix.

## Slide 2 — Contexte

Je pars du contexte de l'hôpital : pics d'activité saisonniers, saturation
des urgences, manque de personnel, risques de rupture de stock en cas de
crise. L'objectif du projet, c'est de construire un dataset structuré à
partir des seuls documents disponibles (les 3 rapports "Chiffres Clés"
2012/2015/2016), d'en tirer une prévision d'activité et une simulation de
crise sanitaire, et de restituer tout ça dans une infographie compréhensible
sans jargon technique.

Un point que je veux poser dès le début, parce que ça va revenir tout le
long : les rapports sources ne donnent que des totaux annuels, donc tout le
reste — la répartition mensuelle, la crise — est une hypothèse de
modélisation que j'assume, pas une donnée mesurée.

## Slides 3-8 — Démonstration du dashboard (live)

Je ne vais pas dérouler toutes les pages en détail, juste un parcours qui
montre les points attendus par l'énoncé (bascule Normal/Crise, filtres de
dates, pas de jargon math).

Parcours que je prévois (`streamlit run app.py`) :

1. Vue d'ensemble, mode Normal — l'état actuel de PSL-CFX (capacité,
   urgences, effectifs).
2. Urgences & Activité, mode Normal, granularité mensuelle — le pic
   hivernal (déc-jan-fév). Je montre aussi l'avertissement affiché sur cet
   onglet (la façon de compter a changé entre 2015 et 2016) : c'est une
   preuve de rigueur, je préfère le mettre en avant que le cacher.
3. Je bascule en mode Crise sur la même page — le profil change de forme
   (pic au printemps, rebond en novembre) et le volume grimpe. J'explique
   simplement : on modélise une vague épidémique, pas juste un pourcentage
   uniforme dans le temps.
4. Je coche "Afficher une estimation pour l'année suivante" pour montrer la
   courbe de prévision qui se prolonge.
5. Page RH — même logique de transparence avec l'avertissement sur les
   effectifs.
6. Sur une page au choix, je montre les filtres Site (PSL / CFX / Total) et
   granularité (mensuel / trimestriel / annuel).

## Slide 9 — Choix techniques et analytiques

Ce que je veux expliquer :

- L'extraction et la structuration du dataset : un schéma commun (ANNEE,
  INDICATEUR, SOUS-INDICATEUR, PLF, CFX, TOTAL, UNITE), 6 domaines couverts,
  et pourquoi j'ai laissé le domaine Qualité de côté (des taux plafonnés à
  100 %, incompatibles avec un coefficient multiplicatif).
- L'interpolation inter-annuelle pour combler 2011/2013/2014/2017 — et sa
  limite : c'est juste une droite entre deux points connus, pas une vraie
  logique métier.
- La saisonnalité mensuelle, qui reste une hypothèse assumée (hiver = pic ;
  crise = vague épidémique), pas une donnée mesurée.
- La simulation de crise : un coefficient par domaine que j'ai sourcé sur
  des données réelles COVID (DREES, ATIH, Cour des comptes, Assemblée
  nationale) plutôt que de l'inventer au jugé. Deux chiffres à garder en
  tête : +14,5 % de lits de réanimation en France en 2020 (proche du +15 %
  que j'ai retenu pour la capacité), et jusqu'à 250 % de la capacité de
  réanimation nécessaire en Île-de-France au printemps 2020.
- Le modèle SARIMA : pourquoi ce modèle (recommandé par l'énoncé, standard
  pour une saisonnalité mensuelle), et sa limite que j'assume — il apprend
  sur une série reconstruite, pas observée, donc sa valeur est surtout
  démonstrative tant que je n'ai pas de vraies données mensuelles.

## Slides 10-11 — Résultats du modèle prédictif + recommandations

Je montre la figure de prévision (historique + prévision + intervalle de
confiance), en expliquant simplement ce que représente l'intervalle. Puis
la figure de diagnostics, sans détailler chaque panneau — juste pour
montrer que j'ai vérifié les résidus du modèle et repéré une anomalie qui
confirme un point de méthode déjà identifié (le saut à la jonction
2015-2016 dû à la reconstruction PLF/CFX des urgences).

Pour les recommandations, je reprends l'essentiel du rapport de mise en
place : renfort saisonnier calé sur le pic hivernal et extension des
filières d'aval à court terme, diversification des fournisseurs d'EPI et
lits tampons ciblés soins critiques à moyen terme, mécanisme de financement
d'urgence pré-négocié et meilleure collecte de données à long terme. Un
point que je veux citer : le retour d'expérience réel de PSL-CFX (les
attentats du 13 novembre 2015, le Plan NOVI-H) comme base de plan de
mobilisation — bien plus solide qu'une hypothèse générique.

## Slide 12 — Limites et perspectives

Je n'ai que 3 années sources, donc toute extrapolation reste fragile. Deux
ruptures de méthode ne peuvent pas être réconciliées avec les sources
disponibles (Urgences, Médecins ETP) — je préfère les documenter et les
afficher dans l'app plutôt que les masquer. Le coefficient "Finances"
(+30 %) est volontairement plus prudent que la moyenne nationale réelle
(environ 3 %), à faire évoluer selon l'usage visé.

Comme perspectives, j'aimerais intégrer des données mensuelles réelles si
elles deviennent accessibles (SAE, ATIH, data.gouv.fr), recalibrer la
saisonnalité sur des données observées, étendre le domaine Qualité avec une
logique additive plafonnée, et automatiser la génération de l'export Excel.

## Slide 13 — Questions

Questions que je m'attends à recevoir, et comment j'y répondrais :

- Pourquoi ces coefficients précis et pas d'autres ? → je reviens sur les
  sources citées en slide 9 et dans le rapport technique.
- Le modèle SARIMA sert-il vraiment à quelque chose si la série est
  reconstruite ? → j'assume la limite, j'insiste sur la valeur
  méthodologique et démonstrative.
- Qu'est-ce que je ferais avec plus de temps ou de données ? → je reviens
  sur les perspectives de la slide 12.
