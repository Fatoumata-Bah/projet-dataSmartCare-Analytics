# Rapport de mise en place — PSL-CFX

Ce rapport présente mes propositions pour gérer les afflux de patients et se
préparer aux risques de crise sanitaire, à partir de ce que montrent les
données du dashboard.

## 1. Constat — ce que montrent les données

Chiffres extraits du dashboard, sur la dernière année réellement observée
dans les rapports sources (2016) — voir le rapport technique pour le détail
des hypothèses de saisonnalité et de crise derrière ces chiffres.

**Urgences.** En mode Normal, le profil mensuel simulé place le pic
d'affluence en décembre-janvier-février (hiver), cohérent avec la
saisonnalité grippale et les décompensations hivernales. En mode Crise, le
profil change complètement de forme : le pic se déplace en mars-avril
(première vague), avec un second pic en novembre (deuxième vague) — le
volume simulé passe de 127 678 à 204 285 passages par an (+60 %, le
coefficient est justifié dans le rapport technique). Le mois d'avril simulé
en crise (environ 38 800 passages) représente à lui seul plus de 2,5 fois le
pic hivernal normal (environ 15 300 en décembre).

**Pathologies dominantes.** Les pathologies cancéreuses (59 017 séjours en
2016), neurologiques (27 748) et cardio-vasculaires (15 938) concentrent
l'essentiel de la charge d'hospitalisation. Ce sont les filières à
sécuriser en priorité en cas de tension sur les lits, parce que ce sont des
prises en charge lourdes et peu déprogrammables.

**Capacité (lits).** 2 229 lits en mode Normal, contre 2 563 lits
nécessaires en mode Crise simulé, soit +334 lits à mobiliser (lits tampons,
déprogrammation, réouverture de capacité).

**RH.** 7 879 ETP paramédicaux (sur un périmètre comparable reconstitué,
voir rapport technique) en mode Normal, contre 8 667 ETP nécessaires en
Crise, soit +788 ETP à mobiliser (renforts, réservistes, heures
supplémentaires).

**Finances.** 887,3 M€ de dépenses d'exploitation en mode Normal, contre
1 153,5 M€ simulés en Crise, soit +266 M€ de surcoût à anticiper.

**Logistique.** 1 123 tonnes de DASRIA (déchets à risque infectieux) en
mode Normal, contre 1 404 tonnes en Crise, soit +281 tonnes — un bon
indicateur proxy de la surconsommation d'équipements de protection à
anticiper.

## 2. Propositions pour gérer les afflux de patients (pics saisonniers)

**Renfort de personnel anticipé sur les mois à risque.** Le profil de
saisonnalité que j'ai utilisé situe le pic hivernal sur
décembre-janvier-février. Il serait logique de planifier les congés du
personnel soignant et les astreintes en conséquence — éviter les
concentrations de congés sur cette période, prévoir un renfort temporaire
ciblé — plutôt qu'un renfort uniforme toute l'année.

**Filières d'aval urgences → services pour réduire l'engorgement.** Les
rapports sources 2015 et 2016 de PSL-CFX documentent déjà ce type d'action
avec des résultats concrets : le rapport 2016 indique que "le renforcement
des filières internes d'aval des urgences a permis... d'assurer un turn
over satisfaisant au sein de l'UHCD du SAU et d'éviter les transferts...
(taux de transfert des urgences le plus faible de l'AP-HP)". C'est un
levier déjà éprouvé sur cet établissement précis, donc le pérenniser et
l'étendre me semble plus fiable qu'une mesure nouvelle jamais testée.

**Centrales d'appel pour la prise de rendez-vous.** Également mentionnées
dans le rapport 2016 comme facilitant l'accès aux consultations — un levier
pour lisser la demande de consultations externes en dehors des pics.

**Suivi trimestriel du taux d'occupation par pôle.** Les données de
capacité par pôle (2012/2015) montrent des taux d'occupation très
hétérogènes selon les pôles (de 64 % à plus de 99 % en 2012). Un
redéploiement de lits entre pôles en période de tension est probablement
plus rapide à activer qu'une ouverture de capacité neuve.

## 3. Propositions pour se préparer aux risques de crise sanitaire

En m'appuyant sur le mode "Crise" du dashboard et sur le retour d'expérience
réel de PSL-CFX :

**Plan de mobilisation RH** (+788 ETP paramédicaux simulés). Réservistes
sanitaires, astreintes renforcées, accords-cadres avec l'intérim médical.
Le rapport 2015 de PSL-CFX documente un précédent réel et directement
comparable : la mobilisation du pôle PRAGUES lors des attentats du 13
novembre 2015 (accueil de 53 victimes, "Plan NOVI-H", retour d'expérience
publié dans les *Annales françaises de médecine d'urgence* en février
2016). Ce retour d'expérience existant est une base bien plus solide qu'une
hypothèse générique pour bâtir un plan de mobilisation propre à
l'établissement.

**Stocks tampons de matériel et d'équipements de protection** (+281 tonnes
de DASRIA simulées, un proxy de la surconsommation de consommables/EPI).
Contrats-cadres avec plusieurs fournisseurs pour éviter la dépendance à un
seul circuit d'approvisionnement — une des causes documentées des ruptures
de stock EPI en 2020 au niveau national — et un stock de sécurité
dimensionné sur ce delta.

**Lits tampons et déprogrammation ciblée** (+334 lits simulés). Je
prioriserais la flexibilité sur les capacités de réanimation/soins
critiques, dont la hausse réelle en Île-de-France en 2020 (jusqu'à 250 %
des besoins par rapport à la capacité fin 2019) a largement dépassé la
moyenne de +15 % modélisée ici sur l'ensemble des lits. Un protocole de
déprogrammation des soins non urgents (la chirurgie ambulatoire
notamment, qui représente 57 % du MCO en 2015) reste le levier le plus
rapide pour libérer des lits.

**Ligne budgétaire d'urgence** (+266 M€ simulés). Provisionner une réserve
de trésorerie mobilisable rapidement, en s'appuyant sur le mécanisme déjà
utilisé au niveau national pendant la crise COVID (financement
complémentaire de l'Assurance Maladie pour compenser surcoûts et pertes
d'activité) plutôt que d'attendre un dispositif ad hoc.

**Calendrier de vigilance aligné sur le profil de crise simulé.** Le profil
"vague épidémique" du dashboard place les pics en mars-avril et en
novembre — il serait logique de caler les revues de préparation (stocks,
RH, lits) sur ce calendrier plutôt que sur un cycle uniforme.

## 4. Priorisation / feuille de route

### Court terme (0-6 mois, faible coût, activable rapidement)

1. Formaliser et documenter le calendrier de renfort saisonnier (déc.-fév.)
   pour les urgences, en s'appuyant sur les plannings existants.
2. Étendre les filières d'aval urgences → services et les centrales d'appel
   (déjà en place et efficaces sur PSL-CFX) à l'ensemble des pôles qui n'en
   bénéficient pas encore.
3. Constituer un annuaire à jour de réservistes/intérimaires mobilisables,
   sur le modèle du retour d'expérience du Plan NOVI-H de 2015.

### Moyen terme (6-18 mois, nécessite un budget dédié)

1. Diversifier les fournisseurs d'EPI/consommables et dimensionner un stock
   de sécurité correspondant au delta de crise simulé.
2. Identifier et pré-qualifier les lits "tampons" mobilisables en priorité
   (avec un focus soins critiques/réanimation) et le protocole de
   déprogrammation associé.
3. Provisionner une ligne budgétaire de réserve pour crise sanitaire.

### Long terme (18 mois+, structurel)

1. Renégocier avec l'ARS/AP-HP un mécanisme de financement d'urgence
   pré-négocié plutôt que découvert au moment de la crise, sur le modèle du
   dispositif national 2020-2023.
2. Recueillir, au fil des prochains rapports "Chiffres Clés", des données
   plus fines (mensuelles si possible) pour remplacer les hypothèses de
   saisonnalité et de crise du dashboard par des données réellement mesurées
   sur PSL-CFX.

Cette feuille de route découle directement des écarts Normal/Crise mesurés
dans le dashboard interactif. Elle a vocation à être revue et priorisée
avec les équipes médicales, RH et logistiques de PSL-CFX, qui connaissent
les contraintes budgétaires et organisationnelles réelles de l'établissement
mieux qu'une analyse de données seule ne peut le refléter.
