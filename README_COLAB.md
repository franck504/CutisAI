## Guide d'Exécution sur Google Colab 🚀

### Cellule 1 : Connexion au Google Drive
*(Autorise l'accès à ton Drive pour sauvegarder les images)*
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Cellule 2 : Clonage du projet GitHub + Installation
```bash
# Se placer dans l'environnement Colab
%cd /content/

# Télécharger le code depuis GitHub (force la mise à jour)
!rm -rf CutisAI
!git clone https://github.com/franck504/CutisAI.git
%cd CutisAI/

# Installation des dépendances
!pip install -q duckduckgo_search pandas requests Pillow tqdm
```

### Cellule 3 : Créer le dossier de destination sur Drive
```python
import os
output_dir = "/content/drive/MyDrive/Projet_Medical/Dataset_Images"
os.makedirs(output_dir, exist_ok=True)
print(f"✅ Dossier prêt : {output_dir}")
```

### Cellule 4 : Lancer le Scraper V2
Le scraper V2 utilise **4 moteurs** (DDG → Bing → Google → Yahoo) et déduplique par SHA256.
```bash
!python scraper.py --csv target_diseases.csv --out "/content/drive/MyDrive/Projet_Medical/Dataset_Images"
```

### Cellule 5 : Analyser le dataset collecté
```bash
!python dataset_stats.py --input "/content/drive/MyDrive/Projet_Medical/Dataset_Images"
```

---

### 💡 Nouveautés V2 :
- **4 moteurs de recherche** : DuckDuckGo, Bing, Google (`udm=2`), Yahoo
- **Déduplication SHA256** : élimine les doublons même avec des URLs différentes
- **Filtrage qualité** : taille min 5 KB, résolution min 100×100 px
- **Mots-clés enrichis** : français + termes médicaux spécialisés (9-12 par maladie)
- **Statistiques JSON** : fichier `scraping_stats.json` généré automatiquement
- **Résilience** : si Colab plante, relancer — le script ne retélécharge pas les images existantes

### ⚠️ Notes importantes :
- Le scraper V2 interroge les **4 moteurs pour chaque mot-clé** (plus d'images mais plus lent)
- Temps estimé : **30-45 minutes** (vs 15-20 min en V1)
- Les images de la V1 déjà sur Drive **ne seront pas re-téléchargées** (reprise automatique)
