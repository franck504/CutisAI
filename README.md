# CutisAI - Collecte et Analyse de Données Dermatologiques

Ce projet regroupe une suite d'outils Python conçus pour la constitution d'un jeu de données (dataset) d'images médicales dermatologiques de haute qualité. Il combine le scraping multi-moteur, l'importation de sources expertes (Kaggle, DermNet NZ) et l'analyse statistique des données récoltées.

## Fonctionnalités principales

- **Scraping Multi-Moteur** : Recherche et téléchargement d'images via Google, Bing, Yahoo et DuckDuckGo avec déduplication par hash SHA256.
- **Importation Experte** : Automatisation de la récupération de datasets certifiés depuis Kaggle.
- **Scraper Spécialisé** : Extraction ciblée d'images médicales sur DermNet NZ.
- **Statistiques et Analyse** : Outil de diagnostic pour vérifier l'équilibre des classes, la résolution des images et les doublons.

## Structure du Projet

- `scraper.py` : Script principal de scraping web multi-moteur.
- `scraper_expert_dermnet.py` : Scraper dédié à la source experte DermNet NZ.
- `import_kaggle.py` : Utilitaire d'importation automatisée pour les datasets Kaggle.
- `dataset_stats.py` : Script d'analyse statistique et de diagnostic du dataset.
- `target_diseases.csv` : Liste des maladies cibles et des mots-clés associés.

## Installation

### Prérequis

- Python 3.8 ou supérieur.
- Un compte Kaggle (pour l'importation automatique).

### Configuration

1. **Installer les dépendances** :
   ```bash
   pip install pandas requests Pillow tqdm beautifulsoup4 duckduckgo_search kaggle
   ```

2. **Configurer l'API Kaggle** :
   Placez votre fichier `kaggle.json` dans le dossier `~/.kaggle/` ou configurez les variables d'environnement `KAGGLE_USERNAME` et `KAGGLE_KEY`.

## Utilisation

### 1. Scraping Web de base
Pour lancer une recherche basée sur le fichier CSV par défaut :
```bash
python scraper.py --csv target_diseases.csv --out ./dataset_images
```

### 2. Importation de sources expertes
Pour récupérer les datasets Kaggle configurés :
```bash
python import_kaggle.py
```

Pour le scraping DermNet NZ :
```bash
python scraper_expert_dermnet.py
```

### 3. Analyse du dataset
Pour obtenir un bilan détaillé des images récoltées :
```bash
python dataset_stats.py --input ./dataset_images
```

## Maintenance

Le projet a été refactorisé pour assurer une maintenance aisée. Les commentaires dans le code sont rédigés en français avec un ton professionnel et explicatif. Aucun emoji n'est utilisé dans les sorties console pour garantir la compatibilité avec tous les environnements d'exécution.
