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
    "manthanshah12/leprosy-chronic-wound-images-co2wounds-v2": "Leprosy",
    "garciaespinoza/skin-disease-raw-dataset": "Scabies",
    "shubhamgoel/dermnet": "General_Derm"  # Sera dispatché plus tard si possible
}

# Dossier final sur le Drive (à adapter dans Colab)
DRIVE_BASE_DIR = "/content/drive/MyDrive/Projet_Medical/Dataset_Images"

def setup_kaggle():
    """Vérifie et configure l'API Kaggle."""
    kaggle_json = Path("/root/.kaggle/kaggle.json")
    if not kaggle_json.exists():
        print("⚠️  Fichier kaggle.json non trouvé dans /root/.kaggle/")
        print("Veuillez uploader votre kaggle.json ou l'instancier manuellement.")
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
    
    for path in src_dir.rglob('*'):
        if path.suffix.lower() in image_extensions:
            # Générer un nom unique court
            with open(path, 'rb') as f:
                h = hashlib.md5(f.read()).hexdigest()[:8]
            
            new_name = f"{prefix}{disease_folder}_{h}{path.suffix}"
            final_path = dest_dir / new_name
            
            if not final_path.exists():
                shutil.move(str(path), str(final_path))
                count += 1
                
    print(f"✅ {count} images expertes ajoutées à {disease_folder}")

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
