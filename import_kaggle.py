import os
import shutil
import json
import zipfile
import hashlib
from pathlib import Path

# ==========================================
# CONFIGURATION DES DATASETS KAGGLE
# ==========================================
# Mapping entre l'identifiant (slug) Kaggle et le dossier de destination
KAGGLE_DATASETS = {
    "joydippaul/mpox-skin-lesion-dataset-version-20-msld-v20": "Mpox_-_Monkeypox",
    "orvile/leprosy-chronic-wound-images-co2wounds-v2": "Leprosy",
    "devdope/skin-disease-raw-dataset": "Scabies",
    "shubhamgoel27/dermnet": "General_Derm"
}

# Dossier final de stockage
BASE_DIR = "./dataset_expert_v2"

def setup_kaggle():
    """
    Vérifie et configure l'accès à l'API Kaggle via les variables d'environnement
    ou le fichier de configuration local.
    """
    # Vérification des identifiants dans les variables d'environnement
    if os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"):
        print("Authentification Kaggle via variables d'environnement détectée.")
        return True

    # Recherche du fichier de configuration standard
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if not kaggle_json.exists():
        print("Attention : Identifiants Kaggle introuvables (ni variables d'environnement, ni kaggle.json).")
        return False
    
    # Sécurisation des permissions pour le client Kaggle
    if os.name != 'nt':
        os.system(f"chmod 600 {kaggle_json}")
        
    try:
        import kaggle
        return True
    except Exception as e:
        print(f"Erreur lors de l'initialisation de l'API Kaggle : {e}")
        return False

def download_dataset(slug, dest_name):
    """
    Télécharge et extrait un jeu de données Kaggle dans un dossier temporaire.
    """
    tmp_dir = Path(f"/tmp/kaggle_{dest_name}")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nTéléchargement du dataset : {slug}...")
    try:
        os.system(f"kaggle datasets download -d {slug} -p {tmp_dir} --unzip")
        return tmp_dir
    except Exception as e:
        print(f"Échec du téléchargement pour {slug} : {e}")
        return None

def move_and_prefix(src_dir, disease_folder, prefix="EXPERT_KAG_"):
    """
    Déplace récursivement les images extraites vers le dossier final de la maladie.
    Ajoute un préfixe pour identifier l'origine de l'image.
    """
    dest_dir = Path(BASE_DIR) / disease_folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    count = 0
    
    # Recherche de toutes les images dans les sous-dossiers extraits
    files_to_move = [p for p in src_dir.rglob('*') if p.suffix.lower() in image_extensions]
    total = len(files_to_move)
    
    print(f"Traitement de {total} images pour la classe {disease_folder}...")
    
    for i, path in enumerate(files_to_move):
        # Calcul d'un hash court pour éviter les collisions de noms de fichiers
        try:
            with open(path, 'rb') as f:
                h = hashlib.md5(f.read()).hexdigest()[:8]
            
            new_name = f"{prefix}{disease_folder}_{h}{path.suffix}"
            final_path = dest_dir / new_name
            
            if not final_path.exists():
                shutil.move(str(path), str(final_path))
                count += 1
            
            # Affichage de la progression par blocs de 50
            if (i + 1) % 50 == 0 or (i + 1) == total:
                print(f"  Progression : {i+1}/{total} images traitées...")
        except Exception:
            continue
                
    print(f"Terminé : {count} images ajoutées à {disease_folder}")

def main():
    print("=" * 60)
    print("AUTOMATISATION DE L'IMPORTATION DES DATASETS KAGGLE")
    print("=" * 60)
    
    if not setup_kaggle():
        print("Impossible de continuer sans identifiants Kaggle valides.")
        return

    # Traitement séquentiel de chaque dataset configuré
    for slug, disease_folder in KAGGLE_DATASETS.items():
        tmp = download_dataset(slug, disease_folder)
        if tmp:
            move_and_prefix(tmp, disease_folder)
            # Nettoyage du dossier temporaire après traitement
            if tmp.exists():
                shutil.rmtree(tmp)

    print("\nProcessus d'importation terminé.")

if __name__ == "__main__":
    # On s'assure que le dossier de destination existe
    os.makedirs(BASE_DIR, exist_ok=True)
    main()
