# Guide d'Exécution CutisAI V2 - Sources Expertes

Ce guide permet de constituer un dataset de haute qualité, composé exclusivement de sources médicales certifiées (Kaggle et DermNet NZ).

## 1. Connexion au Google Drive
```python
from google.colab import drive
drive.mount('/content/drive')
```

## 2. Préparation du Code
```bash
%cd /content/
!rm -rf CutisAI
!git clone https://github.com/franck504/CutisAI.git
%cd CutisAI/

!pip install -q duckduckgo_search pandas requests Pillow tqdm kaggle
```

## 3. Configuration de la destination
```python
import os
output_dir = "/content/drive/MyDrive/Projet_Medical/Dataset_Expert_V2"
os.makedirs(output_dir, exist_ok=True)
print(f"Dossier prêt : {output_dir}")
```

## 4. Importation Kaggle
Utilisez vos identifiants API Kaggle pour importer les datasets médicaux.

```python
import os
os.environ['KAGGLE_USERNAME'] = "votre_nom_utilisateur" 
os.environ['KAGGLE_KEY'] = "votre_token_api" 
!python import_kaggle.py
```

## 5. Scraping DermNet NZ
Récupération des images certifiées sur le site de référence.
```bash
!python scraper_expert_dermnet.py
```

## 6. Statistiques Finales
```bash
!python dataset_stats.py --input "/content/drive/MyDrive/Projet_Medical/Dataset_Expert_V2"
```

## Pourquoi utiliser la V2 ?
- Qualité supérieure : Uniquement des sources médicales validées.
- Traçabilité : Identification claire de l'origine de chaque image via des préfixes.
- Efficacité : Un jeu de données pur améliore les performances d'entraînement des modèles.
