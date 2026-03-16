import os
import shutil
import json
import zipfile
import hashlib
from pathlib import Path

# ==========================================
# CONFIGURATION DES DATASETS KAGGLE
# ==========================================
# Slug -> Destination mapping
KAGGLE_DATASETS = {
    "joydippaul/mpox-skin-lesion-dataset-version-20-msld-v20": "Mpox_-_Monkeypox",
    "orvile/leprosy-chronic-wound-images-co2wounds-v2": "Leprosy",
    "devdope/skin-disease-raw-dataset": "Scabies",
    "shubhamgoel27/dermnet": "General_Derm"
}

# Dossier final sur le Drive (à adapter dans Colab)
DRIVE_BASE_DIR = "/content/drive/MyDrive/Projet_Medical/Dataset_Images"

def setup_kaggle():
    """Vérifie et configure l'API Kaggle (via fichier ou variables d'env)."""
    # 1. Vérifie si les variables d'environnement sont déjà présentes (plus simple sur Colab)
    if os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"):
        print("✅ Identifiants Kaggle détectés via variables d'environnement.")
        return True

    # 2. Sinon, cherche le fichier kaggle.json
    kaggle_dir = Path("/root/.kaggle")
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if not kaggle_json.exists():
        print("⚠️  Identifiants Kaggle manquants (ni variables d'env, ni fichier).")
        return False
    
    os.system("chmod 600 /root/.kaggle/kaggle.json")
    try:
        import kaggle
        return True
    except Exception as e:
        print(f"❌ Erreur import kaggle: {e}")
        return False

def download_dataset(slug, dest_name):
    """Télécharge et extrait un dataset Kaggle."""
    tmp_dir = Path(f"/tmp/kaggle_{dest_name}")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📥 Téléchargement de {slug}...")
    try:
        os.system(f"kaggle datasets download -d {slug} -p {tmp_dir} --unzip")
        return tmp_dir
    except Exception as e:
        print(f"❌ Échec téléchargement {slug}: {e}")
        return None

def move_and_prefix(src_dir, disease_folder, prefix="EXPERT_KAG_"):
    """
    Déplace récursivement les images d'un dossier source vers le dossier maladie cible.
    Ajoute un préfixe pour identifier la source experte.
    """
    dest_dir = Path(DRIVE_BASE_DIR) / disease_folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    count = 0
    
    # Récupérer la liste des fichiers pour calculer le total
    files_to_move = [p for p in src_dir.rglob('*') if p.suffix.lower() in image_extensions]
    total = len(files_to_move)
    
    print(f"📦 Traitement de {total} images expertes pour {disease_folder}...")
    
    for i, path in enumerate(files_to_move):
        # Générer un nom unique court
        with open(path, 'rb') as f:
            h = hashlib.md5(f.read()).hexdigest()[:8]
        
        new_name = f"{prefix}{disease_folder}_{h}{path.suffix}"
        final_path = dest_dir / new_name
        
        if not final_path.exists():
            shutil.move(str(path), str(final_path))
            count += 1
        
        # Log de progression tous les 50 fichiers
        if (i + 1) % 50 == 0 or (i + 1) == total:
            print(f"  ➡️  Progression : {i+1}/{total} images traitées...")
                
    print(f"✅ Terminé : {count} nouvelles images expertes ajoutées à {disease_folder}")

def main():
    print("🚀 AUTOMATION KAGGLE EXPERT DATASETS")
    
    if not setup_kaggle():
        # En mode Colab, on peut donner une alternative
        print("💡 Astuce : Exécutez 'from google.colab import files; files.upload()' pour envoyer kaggle.json")
        return

    for slug, disease_folder in KAGGLE_DATASETS.items():
        tmp = download_dataset(slug, disease_folder)
        if tmp:
            move_and_prefix(tmp, disease_folder)
            shutil.rmtree(tmp)

    print("\n🎉 Fin du processus d'importation Kaggle.")

if __name__ == "__main__":
    main()
