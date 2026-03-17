# 💎 Guide d'Exécution CutisAI V2 — Expert Only

Ce guide permet de constituer un dataset de haute qualité, composé exclusivement de sources médicales certifiées (Kaggle & DermNet NZ), en ignorant le bruit du scraping web général.

---

### 1️⃣ Connexion au Google Drive
```python
from google.colab import drive
drive.mount('/content/drive')
```

### 2️⃣ Installation & Préparation du Code
```bash
# Se placer dans l'environnement Colab
%cd /content/
!rm -rf CutisAI
!git clone https://github.com/franck504/CutisAI.git
%cd CutisAI/

# Installation des dépendances
!pip install -q duckduckgo_search pandas requests Pillow tqdm kaggle
```

### 3️⃣ Créer le dossier V2 (Expert Only)
```python
import os
output_dir = "/content/drive/MyDrive/Projet_Medical/Dataset_Expert_V2"
os.makedirs(output_dir, exist_ok=True)
print(f"✅ Dossier V2 prêt : {output_dir}")
```

---

### 4️⃣ Importation Kaggle (~55 000 images)

#### 🗝️ Configuration des identifiants (Choisir une option)

**A. Via variables d'environnement (Recommandé)**
```python
import os
os.environ['KAGGLE_USERNAME'] = "votre_nom_utilisateur" 
os.environ['KAGGLE_KEY'] = "votre_token_api" 
!python import_kaggle.py
```

**B. Via upload du fichier `kaggle.json`**
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

---

### 5️⃣ Scraping Expert DermNet NZ (Images certifiées)
Ce script récupère les images directement sur le site de référence DermNet NZ avec les noms de maladies inclus.
```bash
!python scraper_expert_dermnet.py
```

---

### 6️⃣ Bilan & Statistiques Finales
Vérifiez l'équilibre des classes et le volume total des données expertes.
```bash
!python dataset_stats.py --input "/content/drive/MyDrive/Projet_Medical/Dataset_Expert_V2"
```

---

### 💡 Pourquoi la V2 ?
- **Qualité 100%** : Aucune image provenant de moteurs de recherche généraux (souvent hors-sujet ou floues).
- **Traçabilité** : Toutes les images sont préfixées par `EXPERT_KAG_` ou `EXPERT_DERMNET_`.
- **Performance** : Un dataset plus petit mais plus pur donne souvent de meilleurs résultats qu'un dataset massif mais bruyant.
