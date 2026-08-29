# Rapport de mise en place — PSL-CFX

> Livrable 2/2 (cf. énoncé) : propositions pour gérer les afflux de patients,
> propositions pour se préparer aux risques de crise sanitaire.

## 1. Constat — ce que montrent les données

Chiffres extraits du dashboard (`app.py`), dernière année réellement observée
dans les rapports sources (2016) — voir `docs/rapport_technique.md` pour le
détail des hypothèses de saisonnalité et de crise sous-jacentes.

- **Urgences** : en mode Normal, le profil mensuel simulé place le pic
  d'affluence en **décembre-janvier-février** (hiver), cohérent avec la
  saisonnalité grippale/décompensations hivernales. En mode Crise, le profil
  change de nature : le pic se déplace en **mars-avril** (première vague) avec
  un second pic en **novembre** (deuxième vague) — le volume simulé passe de
  127 678 à 204 285 passages/an (+60 %, coefficient documenté en rapport
  technique §3.2). Le mois d'avril simulé en crise (≈38 800 passages) représente
  à lui seul plus de 2,5× le pic hivernal normal (≈15 300 en décembre).
- **Pathologies dominantes** : les pathologies cancéreuses (59 017 séjours en
  2016), neurologiques (27 748) et cardio-vasculaires (15 938) concentrent
  l'essentiel de la charge d'hospitalisation — ce sont les filières à
  sécuriser en priorité en cas de tension sur les lits, car ce sont des prises
  en charge lourdes et peu déprogrammables.
- **Capacité (lits)** : 2 229 lits en mode Normal → 2 563 lits nécessaires en
  mode Crise simulé, soit **+334 lits** à mobiliser (lits tampons,
  déprogrammation, réouverture de capacité).
- **RH** : 7 879 ETP paramédicaux (périmètre comparable reconstitué, cf.
  rapport technique §2.2) en mode Normal → 8 667 ETP nécessaires en Crise,
  soit **+788 ETP** à mobiliser (renforts, réservistes, heures
  supplémentaires).
- **Finances** : 887,3 M€ de dépenses d'exploitation en mode Normal → 1 153,5 M€
  simulés en Crise, soit **+266 M€** de surcoût à anticiper.
- **Logistique** : 1 123 tonnes de DASRIA (déchets à risque infectieux) en
  mode Normal → 1 404 tonnes en Crise, soit **+281 tonnes**, un bon indicateur
  proxy de la surconsommation d'équipements de protection à anticiper.

## 2. Propositions pour gérer les afflux de patients (pics saisonniers)

- **Renfort de personnel anticipé sur les mois à risque** : le profil de
  saisonnalité (`DEFAULT_MONTH_PCT_NORMAL` dans `data/pipeline.py`) situe le
  pic hivernal sur décembre-janvier-février. Planifier les congés du
  personnel soignant et les astreintes en conséquence (éviter les
  concentrations de congés sur cette période, renfort temporaire ciblé),
  plutôt qu'un renfort uniforme toute l'année.
- **Filières d'aval urgences → services pour réduire l'engorgement** : les
  rapports sources 2015 et 2016 de PSL-CFX documentent déjà ce type d'action
  avec des résultats concrets — le rapport 2016 indique que "le renforcement
  des filières internes d'aval des urgences a permis... d'assurer un turn
  over satisfaisant au sein de l'UHCD du SAU et d'éviter les transferts...
  (taux de transfert des urgences le plus faible de l'AP-HP)"
  (`SLP-CHF2016.pdf`, "Grands projets"). C'est un levier déjà éprouvé sur cet
  établissement précis : le pérenniser et l'étendre est plus fiable qu'une
  mesure nouvelle non testée.
- **Centrales d'appel pour la prise de rendez-vous** : également mentionnées
  dans le rapport 2016 comme facilitant l'accès aux consultations — un levier
  pour lisser la demande de consultations externes en dehors des pics.
- **Suivi trimestriel du taux d'occupation par pôle** : les données de
  capacité par pôle (2012/2015) montrent des taux d'occupation très
  hétérogènes selon les pôles (de 64 % à plus de 99 % en 2012) — un
  redéploiement de lits entre pôles en période de tension est probablement
  plus rapide à activer qu'une ouverture de capacité neuve.

## 3. Propositions pour se préparer aux risques de crise sanitaire

En s'appuyant sur le mode "Crise" du dashboard (coefficients par domaine,
justifiés dans `docs/rapport_technique.md` §3.2) et sur le retour d'expérience
réel de PSL-CFX :

- **Plan de mobilisation RH** (+788 ETP paramédicaux simulés) : réservistes
  sanitaires, astreintes renforcées, accords-cadres avec l'intérim médical.
  Le rapport 2015 de PSL-CFX documente un précédent réel et directement
  comparable : la **mobilisation du pôle PRAGUES lors des attentats du 13
  novembre 2015** (accueil de 53 victimes, "Plan NOVI-H", retour d'expérience
  publié dans les *Annales françaises de médecine d'urgence*, février 2016).
  Ce retour d'expérience existant est une base bien plus solide qu'une
  hypothèse générique pour bâtir un plan de mobilisation propre à
  l'établissement.
- **Stocks tampons de matériel et d'équipements de protection** (+281 tonnes
  de DASRIA simulées → proxy de la surconsommation de consommables/EPI) :
  contrats-cadres avec plusieurs fournisseurs (éviter la dépendance à un seul
  circuit d'approvisionnement, une des causes documentées des ruptures de
  stock EPI en 2020 au niveau national) et stock de sécurité dimensionné sur
  ce delta.
- **Lits tampons et déprogrammation ciblée** (+334 lits simulés) : prioriser
  la flexibilité sur les capacités de réanimation/soins critiques, dont la
  hausse réelle en Île-de-France en 2020 (jusqu'à 250 % des besoins vs
  capacité fin 2019, source DREES/Assemblée nationale — cf. rapport
  technique §3.2) a largement dépassé la moyenne de +15 % modélisée ici sur
  l'ensemble des lits. Un protocole de déprogrammation des soins non urgents
  (chirurgie ambulatoire notamment, qui représente 57 % du MCO en 2015) est
  le levier le plus rapide pour libérer des lits.
- **Ligne budgétaire d'urgence** (+266 M€ simulés) : provisionner une réserve
  de trésorerie mobilisable rapidement, en s'appuyant sur le mécanisme déjà
  utilisé au niveau national pendant la crise COVID (financement complémentaire
  de l'Assurance Maladie pour compenser surcoûts et pertes d'activité, cf.
  rapport Cour des comptes 2023) plutôt que d'attendre un dispositif ad hoc.
- **Calendrier de vigilance aligné sur le profil de crise simulé** : le
  profil "vague épidémique" du dashboard place les pics en mars-avril et en
  novembre — caler les revues de préparation (stocks, RH, lits) sur ce
  calendrier plutôt que sur un cycle uniforme.

## 4. Priorisation / feuille de route

### Court terme (0-6 mois, faible coût, activable rapidement)

1. Formaliser et documenter le calendrier de renfort saisonnier (déc.-fév.)
   pour les urgences, en s'appuyant sur les plannings existants.
2. Étendre les filières d'aval urgences → services et les centrales d'appel
   (déjà en place et documentées comme efficaces sur PSL-CFX) à l'ensemble
   des pôles n'en bénéficiant pas encore.
3. Constituer un annuaire à jour de réservistes/intérimaires mobilisables,
   sur le modèle du retour d'expérience Plan NOVI-H de 2015.

### Moyen terme (6-18 mois, nécessite un budget dédié)

1. Diversifier les fournisseurs d'EPI/consommables et dimensionner un stock
   de sécurité correspondant au delta de crise simulé.
2. Identifier et pré-qualifier les lits "tampons" mobilisables en priorité
   (avec un focus soins critiques/réanimation) et le protocole de
   déprogrammation associé.
3. Provisionner une ligne budgétaire de réserve pour crise sanitaire.

### Long terme (18 mois+, structurel)

1. Renégocier avec l'ARS/AP-HP un mécanisme de financement d'urgence
   pré-négocié (plutôt que découvert au moment de la crise), sur le modèle
   du dispositif national 2020-2023.
2. Recueillir, au fil des prochains rapports "Chiffres Clés", des données
   plus fines (mensuelles si possible) pour remplacer les hypothèses de
   saisonnalité et de crise du dashboard par des données réellement mesurées
   sur PSL-CFX (cf. limites méthodologiques, `docs/rapport_technique.md` §5).

Cette feuille de route découle directement des écarts Normal/Crise mesurés
dans le dashboard interactif ; elle doit être revue et priorisée avec les
équipes médicales, RH et logistiques de PSL-CFX, qui connaissent les
contraintes budgétaires et organisationnelles réelles de l'établissement
mieux qu'une analyse de données seule ne peut le refléter.
