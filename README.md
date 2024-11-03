# DATASET-FOOTBALL

## Description

Créer un dataset qui fournit des statistiques historiques sur les matchs de football.

### Statistiques à Collecter

- **Nombre de passes** effectuées
- **Nombre de tirs** au but
- **Pourcentage de possession**
- **Cartons jaunes** et **fautes** commises
- **Nombre de corners** tirés
- **Tirs cadrés** et **tirs non cadrés**
- **Temps de possession moyen**
- **Nombre d'interceptions** et **tacles réussis**

### Données Supplémentaires

- Récupération des **futurs matchs** des équipes.
- Mettre à jour les données d'un match dès qu'il est terminé.
- Classer les matchs des équipes européennes par championnat et également par équipes elles-mêmes afin de faciliter les manipulations.
- Automatiser tout le processus

- **Ligues de football** à inclure dans le dataset, comme :
  - Ligue 1
  - Premier League
  - La Liga
  - Serie A
  - Bundesliga
  - Ligue des champions
  - et bien d'autres ....

Ce code illustre comment scraper les divers championnats à utiliser pour notre dataset.

Ceci est un exemple de code que j'ai écrit pour scraper les données. Vous pouvez vous en servir pour récupérer toutes les informations des championnats comme je le montre dans ma vidéo YouTube ci-dessous. Je vous recommande de suivre la vidéo pour mieux comprendre l'idée.

Lien vers la vidéo YouTube : [https://www.youtube.com/watch?v=tzM_TEbp0OE](https://www.youtube.com/watch?v=tzM_TEbp0OE)

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/Arnel7/dataset-football.git

   ```

2. Prérequis:

   Vous avez besoin de `GNU Make` pour:

   - mettre en place votre environnement
   - installer les dépendances
   - executer le code présent dans ce projet

   si vous utilisez `linux` vous pouvez vérifier que votre installation est à jour jour avec cette commande

   ```bash
      make --version
   ```

   Cependant si vous utilisez windows vous pouvez vous reférer au guide d'installation suivant [make for Windows](https://gnuwin32.sourceforge.net/packages/make.htm)

   > ⚠️ **Attention** : Vérifiez votre installation `python` et le gestionnaire de package `pip`.

3. Mise en place de l'environnement et installation des dépendances :

   ```bash
      make setup
   ```

   > vous pouvez voir toutes les commandes disponibles avec

   ```bash
      make
   ```

4. Créez une base de données SQL nommée "football" et importez la base de donnée qui se trouve dans le projet.

5. Groupe de discussion Telegram : [https://t.me/+i1lvynnUuexkZjBk](https://t.me/+i1lvynnUuexkZjBk)

6. Faites vos améliorations et proposez de nouvelles solutions.

## NB : Si le navigateur vous demande de choisir un moteur de recherche lorsque vous lancez le script, veuillez choisir Google.

Bon code à tous !
