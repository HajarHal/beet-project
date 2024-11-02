# beet-project

## Projet d'Identification des Terres Propices à la Culture de Betteraves Sucrières

### Contexte

Cosumar est un acteur clé dans la production de sucre au Maroc. Afin d'optimiser la production de betteraves sucrières et de renforcer ses partenariats, il est essentiel d'identifier les terres les plus adaptées à leur culture. Ce projet vise à maximiser la production de betteraves tout en minimisant les risques d'investissement.

### Objectifs du Projet

- **Identification des Terres Propices :** Utiliser des données climatiques, des propriétés du sol et des images satellites (MODIS) pour évaluer la qualité des terres pour la culture de betteraves.
  
- **Maximisation de la Production :** Développer un modèle prédictif capable d'identifier les zones ayant le meilleur potentiel de rendement en betteraves sucrières.
  
- **Réduction des Risques d'Investissement :** Fournir des recommandations sur les partenariats à établir avec les exploitations agricoles disposant des meilleures terres, afin de sécuriser les investissements de Cosumar.

### Méthodologie

#### Collecte des Données

- Extraction de données à partir de sources variées telles que MODIS, des données climatiques et des propriétés du sol.
- Automatisation de l'extraction des données à l'aide d'Apache Airflow.

#### Transformation des Données

- Utilisation de Google Cloud Dataproc pour effectuer des transformations sur les données brutes, incluant le nettoyage, la normalisation et l'ingénierie des caractéristiques.

#### Stockage des Données

- Les données traitées sont stockées dans Google BigQuery pour une analyse facile et rapide.

#### Modélisation

- Développement d'un modèle de classification sur Vertex AI pour prédire la capacité des terres à soutenir la culture de betteraves sucrières.
- Déploiement du modèle pour faciliter les prédictions en temps réel.

#### Création d'une Application Web

- Développement d'une application Flask pour permettre aux utilisateurs de prédire la qualité des terres et visualiser les résultats sur une carte interactive.

### Résultats Attendus

- Une base de données complète des terres identifiées comme étant propices à la culture de betteraves sucrières.
- Un modèle prédictif validé qui pourra être utilisé pour prendre des décisions éclairées sur les investissements futurs.
- Une interface utilisateur intuitive pour visualiser et interagir avec les données sur les terres agricoles.

### Conclusion

Ce projet constitue une avancée stratégique pour Cosumar, en lui permettant d'optimiser ses ressources et de prendre des décisions basées sur des données concrètes pour le développement de la culture de betteraves sucrières au Maroc. En identifiant les terres les plus appropriées et en établissant des partenariats avec des exploitations agricoles qualifiées, Cosumar pourra maximiser sa production tout en minimisant les risques financiers.
