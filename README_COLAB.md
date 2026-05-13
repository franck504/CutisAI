# Guide d'utilisation sur Google Colab

Ce guide détaille les étapes pour exécuter les outils CutisAI dans un environnement Google Colab.

## 1. Préparation de l'environnement

### Connexion au Google Drive
Cette étape permet de sauvegarder les images directement sur votre espace de stockage persistant.
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Installation du projet et des dépendances
```python
# Se placer dans l'espace de travail
%cd /content/
!rm -rf CutisAI
!git clone https://github.com/franck504/CutisAI.git
%cd CutisAI/

# Installation des bibliothèques nécessaires
!pip install -q duckduckgo_search pandas requests Pillow tqdm beautifulsoup4 kaggle
```

## 2. Configuration des sources expertes

### Importation depuis Kaggle
Pour utiliser l'API Kaggle, vous devez fournir vos identifiants.

**Option A : Utilisation des variables d'environnement**
```python
import os
os.environ['KAGGLE_USERNAME'] = "votre_nom_utilisateur"
os.environ['KAGGLE_KEY'] = "votre_cle_api"

!python import_kaggle.py
```

**Option B : Chargement du fichier kaggle.json**
```python
import os
from google.colab import files

if not os.path.exists("/root/.kaggle/kaggle.json"):
    uploaded = files.upload()
    if "kaggle.json" in uploaded:
        os.makedirs("/root/.kaggle", exist_ok=True)
        with open("/root/.kaggle/kaggle.json", "wb") as f:
            f.write(uploaded["kaggle.json"])
        os.chmod("/root/.kaggle/kaggle.json", 0o600)

!python import_kaggle.py
```

## 3. Exécution des scrapers spécialisés

### Scraping DermNet NZ
```python
!python scraper_expert_dermnet.py
```

### Scraping Multi-moteur (Web)
```python
!python scraper.py --out "/content/drive/MyDrive/Dataset_CutisAI"
```

## 4. Analyse et Statistiques
Pour obtenir un rapport complet sur le dataset généré :
```python
!python dataset_stats.py --input "/content/drive/MyDrive/Dataset_CutisAI"
```

---

**Notes importantes :**
- L'utilisation de préfixes (ex: `EXPERT_KAG_`) permet de garantir la traçabilité des sources.
- Veillez à respecter les limites de requêtes des moteurs de recherche en ne lançant pas plusieurs sessions de scraping simultanément.
