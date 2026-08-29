# Rapport technique — PSL-CFX

Ce rapport présente les sources que j'ai utilisées, les traitements que j'ai
appliqués au dataset, et les choix de modélisation que j'ai retenus pour ce
projet.

## 1. Sources des données

J'ai travaillé à partir des 3 rapports "Chiffres Clés" annuels des Hôpitaux
Universitaires Pitié-Salpêtrière — Charles Foix (AP-HP), disponibles dans
`sources/` :

- `SLP-CHF2012.pdf` — Chiffres Clés 2012
- `SLP-CHX2015.pdf` — Chiffres Clés 2015
- `SLP-CHF2016.pdf` — Chiffres Clés 2016

Ces rapports ne donnent que des totaux **annuels** : il n'y a aucune
décomposition mensuelle ou journalière dans les documents fournis. C'est la
contrainte de départ qui explique une bonne partie des choix décrits plus
loin.

## 2. Extraction et structuration du dataset

J'ai retenu un schéma commun à tous les domaines : `ANNEE, INDICATEUR,
SOUS-INDICATEUR, PLF, CFX, TOTAL, UNITE`, un fichier par domaine dans
`data/<domaine>/<domaine>-data.csv`, généré par `data/build_raw.py`.

6 domaines sont couverts : Activité & Service, Patients (pathologies),
Capacité (lits), Finances, RH, Logistique. J'ai volontairement laissé de
côté le domaine Qualité (indicateurs IPAQSS) — j'explique pourquoi en 4.3.

### 2.1 Traçabilité par domaine

Pour pouvoir retrouver facilement d'où vient chaque chiffre, voici la
correspondance entre indicateur et page du rapport source :

| Domaine | Sous-indicateur | Années | Page source |
| --- | --- | --- | --- |
| Activité & Service | Urgences — Passages totaux | 2011, 2012, 2015, 2016 | 2012 p.4 ; 2015 p.7 ; 2016 p.4 |
| Activité & Service | Urgences — Patients admis en hospitalisation | 2011, 2012, 2015 | 2012 p.4 ; 2015 p.7 |
| Activité & Service | Consultations externes | 2012, 2015, 2016 | 2012 p.2/4 ; 2015 p.6 ; 2016 p.4 |
| Activité & Service | Séjours HC (>24h) / Ambulatoire (<24h) | 2012, 2015, 2016 | 2012 p.4 ; 2015 p.6 ; 2016 p.4 |
| Activité & Service | Actes opératoires | 2016 | 2016 p.4 |
| Activité & Service | Naissances / Greffes | 2012, 2015, 2016 | 2012 p.1 ; 2015 p.15 ; 2016 p.4 |
| Patients | 9 causes d'hospitalisation (nb de séjours) | 2012, 2015 | 2012 p.3 ; 2015 p.5 |
| Capacité | Lits totaux + répartition MCO/SSR/SLD/PSY | 2012, 2015, 2016 | 2012 p.3 ; 2015 p.4 ; 2016 p.4 |
| Finances | Dépenses d'exploitation / Recettes | 2012, 2015, 2016 | 2012 p.4 ; 2015 p.9 ; 2016 p.4 |
| RH | Médecins (ETP / effectif physique), Personnel paramédical (ETP) | 2012, 2015, 2016 | 2012 p.2 ; 2015 p.10 ; 2016 p.4 |
| Logistique | Restauration, DASRIA, DAOM/DMA | 2012, 2015 | 2012 p.2 ; 2015 p.11 |

### 2.2 Erreurs corrigées en repassant sur les données

En recomparant mes CSV aux PDF sources, j'ai trouvé et corrigé quelques
erreurs :

- "Actes opératoires" (47 925) était rattaché à 2015 dans ma première
  version, alors que ce chiffre vient en réalité du rapport 2016
  (`SLP-CHF2016.pdf` p.4) — il n'apparaît nulle part dans le rapport 2015.
- Il me manquait "Patients admis en hospitalisation" pour 2011 (6 083, PSL),
  pourtant donné en toutes lettres p.4 du rapport 2012 — je n'avais repris
  que la valeur de 2012.
- Pour "Consultations externes" 2015, je n'avais saisi que le total (607 950),
  alors que le rapport donne le détail PSL 597 660 / CFX 10 290 (p.6). Ça
  m'évite d'avoir à passer par la reconstruction par ratio décrite plus bas.

## 3. Traitements appliqués

### 3.1 Interpolation inter-annuelle

`data/pipeline.py::interpolate_annual` comble les années manquantes (2011,
2013, 2014, 2017) par interpolation linéaire entre les points connus (2012,
2015, 2016), avec extrapolation aux bornes. Quand une seule des trois
valeurs PLF/CFX/TOTAL est publiée, je reconstruis les deux autres ; si
aucune année ne donne PLF et CFX en même temps, j'utilise un ratio par
défaut de 0,5 pour répartir le total.

Cette méthode a des limites que je préfère assumer plutôt que cacher :

- L'interpolation linéaire n'a aucune logique métier : c'est juste une
  droite entre deux points connus, elle ne peut pas capter un effet de
  seuil (ouverture d'un service, réorganisation) survenu entre deux
  rapports.
- Certains indicateurs n'ont qu'un seul point connu sur toute la période
  (Actes opératoires, Naissances, Greffes) : ils restent constants sur
  2011-2017 une fois extrapolés. Ce n'est pas vraiment une "tendance", mais
  c'est la meilleure hypothèse neutre disponible avec un seul point.
- Le ratio par défaut à 0,5 reste arbitraire. Pour "Urgences → Passages
  totaux" et "Patients admis en hospitalisation", ce cas se présente parce
  que la nature même des données change d'une année sur l'autre (voir
  ci-dessous) — corriger juste le ratio n'aurait pas réglé le vrai
  problème.

Il y a deux cas où je n'ai pas pu réconcilier les chiffres, et que j'ai
préféré documenter plutôt que forcer une correction artificielle :

Pour "Urgences → Passages totaux", 2011/2012 (83 002 / 85 993) est un
chiffre PSL seul, dans une section intitulée "Les urgences de La
Pitié-Salpêtrière" (2012 p.4). 2015 (121 721) additionne 59 072 passages au
SAU et 62 649 aux urgences dentaires (2015 p.7). 2016 (127 678) se
décompose encore différemment ("dont 61 651 aux urgences spécialisées",
2016 p.4). Ces trois chiffres ne mesurent tout simplement pas la même
chose, donc je ne veux pas laisser leur évolution se lire comme une vraie
série continue — j'ai ajouté un avertissement directement sur cet onglet du
dashboard.

Pour "Médecins (ETP)", 2012 (1 253) et 2015 (1 621) incluent les
internes/résidents/FFI dans le total. Le rapport 2016 (947) les compte à
part ("465 internes" listés séparément) — et comme l'ETP des internes n'est
pas publié pour 2016, je ne peux pas reconstruire un chiffre comparable. Ce
n'est pas une vraie chute d'effectifs, c'est une rupture de définition —
avertissement dans le dashboard là aussi (page RH).

En revanche, pour "Médecins (effectif physique)" et "Personnel paramédical
(ETP)", le rapport 2016 donne le détail des sous-catégories, ce qui m'a
permis de recalculer un chiffre sur un périmètre comparable à 2012/2015 (le
calcul est en commentaire dans `data/build_raw.py`) — donc ces deux-là, j'ai
pu les corriger plutôt que juste les signaler.

### 3.2 Simulation de crise sanitaire

`data/pipeline.py::apply_crisis` applique un coefficient multiplicatif
unique par domaine à la valeur annuelle interpolée. L'énoncé demandait
explicitement de s'appuyer sur des sources réelles sur l'impact du COVID
plutôt que d'inventer des chiffres au jugé, donc j'ai cherché des données
publiques pour étayer chaque coefficient :

| Domaine | Coefficient | Ce que dit la source |
| --- | --- | --- |
| Activité & Service | ×1,6 | Modélise un scénario de tension aiguë sur les urgences et les soins critiques (pas l'activité hospitalière moyenne, voir la nuance plus bas). Je me suis calée sur la fourchette basse des besoins en réanimation observés en Île-de-France au printemps 2020, où les lits nécessaires ont représenté jusqu'à 250 % de la capacité disponible fin 2019 (DREES, ER n°1289 ; Assemblée nationale, QE n°27919/37686). |
| Patients | ×1,8 | Même logique, calibrée un cran au-dessus car cet indicateur suit spécifiquement les pathologies génératrices d'hospitalisations lourdes, proches du profil réanimation, dans la fourchette IDF 140-250 % observée en 2020. |
| Capacité | ×1,15 | Bien sourcé : le nombre de lits de réanimation en France est passé de 5 420 (fin 2019) à 6 210 (fin 2020), soit +14,5 % — quasiment le coefficient retenu (DREES, ER n°1289, déc. 2023). Les lits de réanimation n'étant qu'une fraction des lits "toutes disciplines" de ce dataset, +15 % au global reste un ordre de grandeur cohérent, voire prudent, pour un hôpital d'Île-de-France en première ligne. |
| Finances | ×1,30 | À relativiser : la Cour des comptes chiffre le surcoût national COVID pris en charge par l'Assurance Maladie à 3 Md€ en 2020, soit environ 3 % des dépenses hospitalières publiques nationales — bien en-dessous de +30 %. J'ai gardé un coefficient plus haut parce qu'il représente une hypothèse de planification budgétaire prudente pour un établissement d'Île-de-France, épicentre de la première vague, pas la moyenne nationale. À revoir si l'objectif devient une estimation réaliste plutôt qu'un scénario de préparation au pire cas. |
| RH | ×1,10 | Cohérent avec la hausse observée de l'absentéisme hospitalier pendant la crise (d'environ 9-11 % en 2019 à 10-13 % en 2020-2021 selon la FHF et les retours d'établissements médico-sociaux). Ce n'est pas exactement le même concept que celui modélisé ici (effectifs mobilisés en renfort), mais l'ordre de grandeur (+1 à +3 points, soit environ +10 %) est comparable. |
| Logistique | ×1,25 | Le moins bien sourcé des six : la littérature (HCSP, avis 2020-2021) confirme qualitativement une hausse notable des DASRI dans les régions les plus touchées, mais je n'ai pas trouvé de pourcentage national consolidé pour valider précisément +25 %. À affiner si je trouve une source chiffrée. |

Sources que j'ai utilisées :

- DREES, *Nombre de lits en réanimation : l'adaptation du système hospitalier
  pendant la crise due au Covid-19*, Études et Résultats n°1289, décembre 2023.
- ATIH, *Analyse de l'activité hospitalière 2020 — focus COVID-19*.
- Cour des comptes, *La situation financière des hôpitaux publics après la
  crise sanitaire*, rapport public thématique, octobre 2023.
- Assemblée nationale, questions écrites QE n°27919 et n°37686 (capacité
  réanimation Île-de-France, mars-avril 2020).
- Fédération Hospitalière de France (FHF) / retours d'établissements — taux
  d'absentéisme hospitalier 2019-2020.
- Haut Conseil de la Santé Publique (HCSP), avis sur la gestion des DASRI
  pendant l'épidémie de Covid-19 (2020-2021).

Un point que je veux assumer clairement : ces mêmes sources montrent que
l'activité hospitalière globale a en réalité baissé en 2020 (l'ATIH et la
DREES signalent un recul historique de -17,3 % des passages aux urgences,
lié au confinement et à la déprogrammation des soins non urgents). Le
coefficient ×1,6 que j'ai retenu ne prétend donc pas reproduire la moyenne
observée en 2020, mais modéliser le scénario de saturation des urgences et
des soins critiques — celui que l'énoncé demande explicitement de préparer
("Saturation des services d'urgences", "Ruptures de stocks de matériel",
`sources/Projet_Data_Ko.pdf` p.3), et celui qui sert de base aux
recommandations du rapport de mise en place. C'est un choix de modélisation
que j'assume, pas un raccourci pris sans y réfléchir.

### 3.3 Reconstitution de la saisonnalité mensuelle

`data/pipeline.py::reconstruct_monthly` répartit chaque valeur annuelle sur
12 mois selon un profil assumé, uniquement pour les domaines Activité &
Service et Patients, où une saisonnalité médicale a du sens.

En mode normal (`DEFAULT_MONTH_PCT_NORMAL`), j'ai mis une légère
sur-activité en hiver (décembre-janvier, cohérent avec le pic saisonnier de
grippe et de décompensations hivernales bien documenté par Santé Publique
France) et un second pic plus modéré l'été (traumatologie estivale,
canicule).

En mode crise (`DEFAULT_MONTH_PCT_CRISE`), j'ai repris la forme de la
première vague COVID en Île-de-France : creux en début d'année, montée
brutale au printemps (mars-avril), rechute, puis deuxième vague à l'automne
— le pic de lits de réanimation a été atteint le 15 avril 2020, avec une
proportion de patients COVID en réanimation qui a dépassé 60 % début avril.

Ces deux profils restent des hypothèses de forme, pas des séries mesurées :
aucune des 3 sources annuelles ne permet de vérifier la répartition
infra-annuelle réelle de PSL-CFX. Ils sont cohérents avec la littérature
générale, mais pas calibrés sur des données propres à l'établissement.

## 4. Choix et justification des modèles

### 4.1 Modèle prédictif : SARIMA

`utils.py::forecast_next_year` utilise `SARIMAX(order=(1,1,1),
seasonal_order=(1,1,1,12))` sur la série mensuelle reconstituée, et a besoin
d'au moins 24 points mensuels pour tourner.

#### La prévision en pratique

Cette figure est générée par `docs/generate_figures.py`, qui réutilise
directement `utils.py::fit_forecast_model` — la même fonction que le
dashboard, pas de logique dupliquée — sur la série "Urgences → Passages
totaux" (PLF+CFX, mode Normal), la plus longue et la plus lisible du
dataset :

![Prévision SARIMA — Urgences, passages totaux](figures/forecast_urgences.png)

Le modèle reproduit bien le profil de saisonnalité mensuel que j'ai injecté
en amont (pic récurrent en décembre, creux en milieu d'année) et le
prolonge sur 12 mois, avec un intervalle de confiance à 80 % qui s'élargit
logiquement plus l'horizon de prévision s'éloigne.

#### Diagnostics du modèle

![Diagnostics du modèle SARIMA](figures/forecast_diagnostics.png)

Ce sont les 4 panneaux de diagnostic standard de `statsmodels`
(`results.plot_diagnostics()`) :

- Les résidus standardisés (en haut à gauche) sont globalement centrés sur
  0, sauf un pic net à la jonction 2015-2016 (résidu de plus de 6
  écarts-types). Ce n'est pas un défaut du modèle : c'est la trace directe
  de la limite décrite en 3.1, la répartition PLF/CFX des "Urgences" étant
  reconstruite avec un ratio par défaut faute d'année où les deux valeurs
  sont connues ensemble, ce qui crée un saut artificiel dans la série. Ça
  illustre bien que la fiabilité du modèle dépend de la qualité de la série
  d'entrée, pas d'un mauvais choix d'ordres SARIMA.
- L'histogramme et le Q-Q plot montrent une queue de distribution plus
  épaisse que la normale théorique à droite, cohérent avec ce même point
  isolé qui tire la distribution des résidus vers une asymétrie
  non-gaussienne.
- Le corrélogramme (en bas à droite) ne montre aucune autocorrélation
  résiduelle significative au-delà du premier retard — le modèle capture
  bien la structure temporelle résiduelle, ce point isolé mis à part.

Sur le choix des ordres : (1,1,1) sur la composante non saisonnière capture
une tendance simple avec un terme autorégressif et un terme de moyenne
mobile — un choix standard et raisonnable pour une première itération,
sans sur-paramétrer un modèle sur seulement 7 années de données
reconstruites. La composante saisonnière (1,1,1,12) reprend la même
structure sur une période de 12 mois, cohérente avec le profil mensuel
imposé en amont.

La vraie limite, que je préfère assumer plutôt que présenter le modèle
comme plus solide qu'il ne l'est : la série d'entrée n'est pas une série
observée, c'est la reconstruction décrite en 3.3. Le modèle SARIMA apprend
donc surtout à reproduire le profil de saisonnalité que j'ai moi-même
injecté, avec un peu de bruit lié à l'interpolation inter-annuelle. Sa
valeur est démonstrative — montrer la mécanique d'une prévision saisonnière
— plutôt que vraiment prédictive, tant que le dataset ne contient pas de
données mensuelles réelles.

`enforce_stationarity=False, enforce_invertibility=False` : nécessaire en
pratique car la série reconstruite (interpolation + profil assumé) ne
respecte pas toujours les conditions théoriques de stationnarité d'un
processus ARIMA classique ; sans cette option, `statsmodels` n'arrive pas à
converger sur certaines sous-séries à faible variance.

### 4.2 Simulation de crise : approche multiplicative

J'ai choisi un coefficient unique par domaine plutôt qu'un modèle plus fin
(par exemple une courbe épidémique type SIR, ou une modélisation
différenciée par sous-indicateur), pour deux raisons : la simplicité et la
lisibilité pour un public non technique (l'énoncé demande explicitement
"pas de jargon mathématique / scientifique / informatique"), et le fait que
le dataset source — 3 points annuels — ne contient de toute façon pas assez
d'information pour calibrer un modèle plus riche sans sur-ajuster. Le prix
de cette simplicité, c'est qu'un coefficient unique gomme l'hétérogénéité
réelle observée en 2020 (baisse de l'activité programmée contre explosion
de la réanimation) — je l'assume et je le documente en 3.2.

### 4.3 Exclusion du domaine Qualité

Les indicateurs IPAQSS sont des taux de traçabilité en %, plafonnés à 100.
Un coefficient multiplicatif comme celui utilisé pour les volumes ferait
mécaniquement dépasser 100 % pour toute valeur de départ supérieure à
100/coefficient — ça n'aurait pas de sens. Une approche additive plafonnée
(`min(100, valeur + delta)`) serait nécessaire si je voulais intégrer ce
domaine plus tard.

## 5. Limites générales et pistes d'amélioration

- Je n'ai que 3 années sources, donc toute interpolation ou extrapolation
  reste fragile ; les indicateurs à un seul point connu (Actes opératoires,
  Naissances, Greffes) restent constants sur toute la période reconstituée.
- La saisonnalité et la crise sont des hypothèses de forme documentées, pas
  des données mesurées pour PSL-CFX spécifiquement.
- Deux ruptures de périmètre ne peuvent pas être réconciliées avec les 3
  sources disponibles (Urgences, Médecins ETP) — je les ai signalées dans
  le dashboard plutôt que de les masquer ; obtenir le détail méthodologique
  exact auprès de la direction des Hôpitaux Universitaires PSL-CFX
  permettrait de les corriger vraiment.
- Le coefficient de crise "Finances" (×1,30) est volontairement plus
  prudent que la moyenne nationale observée en 2020 (environ 3 % de
  surcoût, Cour des comptes) : à faire évoluer selon l'usage visé (scénario
  de préparation au pire cas contre estimation réaliste).
- Le coefficient "Logistique" (×1,25) reste le moins solidement sourcé des
  six : une source chiffrée sur l'évolution des DASRI en Île-de-France en
  2020 permettrait de l'affiner.
- Le modèle SARIMA est entraîné sur une série reconstruite, pas observée :
  sa valeur est plus pédagogique/démonstrative que réellement prédictive.
