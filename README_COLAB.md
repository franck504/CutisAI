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

### Cellule 5 : Analyser le dataset (V2 brute)
```bash
!python dataset_stats.py --input "/content/drive/MyDrive/Projet_Medical/Dataset_Images"
```

---

## 🏥 Phase 3 : Intégration de Données Expertes (Optionnel)

### Cellule 6 : Importer les Datasets Kaggle (Validé / Clean)
Cette étape télécharge Mpox v2, Lèpre (plaies) et DermNet depuis Kaggle.
*Nécessite d'uploader votre `kaggle.json` (dans `/root/.kaggle/`).*
```python
# Installation API Kaggle si besoin
!pip install -q kaggle
# Lancement de l'import automation
!python import_kaggle.py
```

### Cellule 7 : Scraper Expert DermNet NZ
Un scraper très ciblé qui récupère les images certifiées directement sur les rubriques spécialisées de DermNet NZ.
```bash
!python scraper_expert_dermnet.py
```

### Cellule 8 : Bilan Final (Expert + Scraped)
Relancez les stats pour voir l'impact des données expertes sur votre dataset.
```bash
!python dataset_stats.py --input "/content/drive/MyDrive/Projet_Medical/Dataset_Images"
```

---

### 💡 Nouveautés V2 & Expert :
- **4 moteurs de recherche** : DuckDuckGo, Bing, Google (`udm=2`), Yahoo
- **Expert Datasets** : Intégration automatisée de Mpox v2.0, Leprosy Chronic Wounds, Scabies (Kaggle).
- **DermNet Expert Scraper** : Récupération ciblée sur un site de référence dermatologique.
- **Identification** : Les images expertes sont préfixées `EXPERT_KAG_` ou `EXPERT_DERMNET_`.

### ⚠️ Notes importantes :
- Le scraper V2 interroge les **4 moteurs pour chaque mot-clé** (plus d'images mais plus lent)
- Temps estimé : **30-45 minutes** (vs 15-20 min en V1)
- Les images de la V1 déjà sur Drive **ne seront pas re-téléchargées** (reprise automatique)
