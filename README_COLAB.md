## Guide d'Exécution sur Google Colab 🚀

Puisque ce script est destiné à être hébergé sur votre **GitHub**, voici exactement les étapes (sous forme de blocs de code à copier/coller) à exécuter dans votre Notebook **Google Colab** pour le faire tourner et sauvegarder sur votre **Google Drive**.

### Cellule 1 : Connexion au Google Drive
*(Cette cellule vous demandera d'autoriser l'accès à votre Drive)*
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Cellule 2 : Clonage de votre Projet GitHub et installation des dépendances
*(Remplacez `VOTRE_LIEN_GITHUB_ICI` par l'URL de votre repo)*
```bash
# 1. On se place dans l'environnement de Colab
%cd /content/

# 2. On télécharge le code depuis votre GitHub
!git clone https://github.com/VOTRE_NOM/VOTRE_REPO.git
%cd VOTRE_REPO/

# 3. Installation des paquets nécessaires au scraping (fast!)
!pip install -q duckduckgo_search pandas requests Pillow tqdm
```

### Cellule 3 : Lancement du Scraper
Le script va s'exécuter en utilisant 15 Threads en se synchronisant sur le fichier CSV. Il va sauvegarder les fichiers **directement dans votre dossier Google Drive**.

*Note : Assurez-vous d'avoir créé le dossier `Projet_Medical/` manuellement sur votre Google Drive.*
```bash
# On lance le script avec :
# --csv : le fichier csv des maladies
# --out : L'emplacement dans votre Google Drive où sauvegarder les images
!python scraper.py --csv target_diseases.csv --out "/content/drive/MyDrive/Projet_Medical/Dataset_Images"
```

### 💡 Avantages de cette méthode :
- **Efficacité** : DuckDuckGo n'a pas besoin de Clés API.
- **Robustesse** : Le script vérifie la taille, le format réel (via `Pillow`) et l'intégrité de chaque image téléchargée.
- **Résilience** : Si Colab plante au milieu (timeout Google), vous relancez. Le code ne retéléchargera pas les images déjà présentes !
- **Multi-Threading** : Les 15 threads permettent de tirer profit de l'excellente connectivité internet des serveurs Google (Téléchargement ultra-rapide sans épuiser la RAM !).
