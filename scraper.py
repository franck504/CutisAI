import os
import argparse
import time
import random
import pandas as pd
import requests
from io import BytesIO
from PIL import Image
from duckduckgo_search import DDGS
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# ==========================================
# CONFIGURATION
# ==========================================
MAX_IMAGES_PER_KEYWORD = 300  # Nombre maximum d'images à chercher par mot-clé
MAX_WORKERS = 15              # Nombre de threads pour le téléchargement parallèle (Idéal Colab)
TIMEOUT = 10                  # Temps d'attente maximum par image (secondes)

def is_valid_image(content):
    """
    Vérifie si le contenu téléchargé est bien une image valide et non corrompue.
    """
    try:
        img = Image.open(BytesIO(content))
        img.verify() # Vérifie l'intégrité du fichier image
        return True
    except Exception:
        return False

def download_image(url, save_path):
    """
    Télécharge une image depuis son URL et la sauvegarde si elle est valide.
    """
    try:
        # User-Agent pour éviter d'être bloqué par certains serveurs
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=TIMEOUT, stream=True)
        response.raise_for_status()
        
        # Vérification stricte
        if not is_valid_image(response.content):
            return False
            
        # Écriture sur le disque (Google Drive si lancé via Colab)
        with open(save_path, 'wb') as f:
            f.write(response.content)
            
        return True
    except Exception:
        return False

def scrape_keyword(keyword, disease_name, output_dir):
    """
    Cherche et télécharge les images pour un mot-clé précis en multi-threading.
    """
    print(f"\n[*] Recherche DDG : '{keyword}'...")
    
    # Création du dossier pour cette maladie (Remplacer espaces par underscores)
    safe_disease_name = str(disease_name).strip().replace(" ", "_").replace("/", "-")
    disease_dir = os.path.join(output_dir, safe_disease_name)
    os.makedirs(disease_dir, exist_ok=True)
    
    try:
        results = []
        # Boucle de retry pour gérer le Ratelimit (403) DuckDuckGo
        for attempt in range(5):
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.images(
                        keyword,
                        region="wt-wt",
                        safesearch="off",
                        size="Medium", # Évite les miniatures minuscules
                        type_image="photo", # Format photo réelle
                        max_results=MAX_IMAGES_PER_KEYWORD
                    ))
                break # On sort de la boucle si succès
            except Exception as e:
                if "403" in str(e) or "Ratelimit" in str(e).lower() or attempt < 4:
                    wait_time = (attempt + 1) * 15 + random.randint(5, 15)
                    print(f"    [!] RateLimit détecté pour le mot-clé. Pause antibot de {wait_time}s (Tentative {attempt+2}/5)...")
                    time.sleep(wait_time)
                else:
                    raise e
            
        if not results:
            print(f"[-] Aucune image trouvée pour '{keyword}'.")
            return 0            
        urls = [res['image'] for res in results]
        print(f"    -> {len(urls)} URLs trouvées. Début du téléchargement (Threads: {MAX_WORKERS})...")
        
        # Préparation des tâches
        tasks = []
        safe_keyword = str(keyword).strip().replace(" ", "_").replace("/", "-").replace("'", "")
        
        for i, url in enumerate(urls):
            # Tenter d'extraire l'extension, sinon forcer .jpg
            ext = url.split('.')[-1].split('?')[0].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                ext = "jpg"
                
            filename = f"{safe_keyword}_{str(i).zfill(3)}.{ext}"
            save_path = os.path.join(disease_dir, filename)
            
            # Ne pas re-télécharger si l'image existe déjà (reprise sur erreur)
            if not os.path.exists(save_path):
                tasks.append((url, save_path))
            
        downloaded = 0
        
        # Téléchargement asynchrone / Multi-Thread
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_url = {executor.submit(download_image, url, path): url for url, path in tasks}
            
            # Barre de progression TQDM
            for future in tqdm(as_completed(future_to_url), total=len(tasks), desc=f"    Tél. {safe_keyword}"):
                if future.result():
                    downloaded += 1
                    
        print(f"[+] Succès : {downloaded}/{len(tasks)} nouvelles images téléchargées pour '{keyword}'.")
        return downloaded
        
    except Exception as e:
        print(f"[-] Erreur critique lors du scraping de '{keyword}': {e}")
        return 0

def main(csv_path, output_dir):
    print("========================================================")
    print("🚀 DÉMARRAGE DU SCRAPER D'IMAGES MÉDICALES (MULTI-THREAD)")
    print("========================================================")
    print(f"📁 Dossier de destination final : {output_dir}")
    print(f"📄 Fichier source CSV : {csv_path}\n")
    
    if not os.path.exists(csv_path):
        print(f"❌ Erreur : Le fichier CSV '{csv_path}' est introuvable !")
        return
        
    df = pd.read_csv(csv_path)
    total_downloaded = 0
    
    for index, row in df.iterrows():
        # Utiliser le nom commun ou le nom scientifique comme nom de dossier
        disease_name = row['common_name_en'] 
        keywords = str(row['search_keywords']).split('|')
        
        print(f"\n========================================================")
        print(f"🧬 MALADIE: {disease_name}")
        print(f"========================================================")
        
        for kw in keywords:
            kw = kw.strip()
            if kw:
                # Pause stratégique entre les requêtes principales pour éviter le ban IP
                time.sleep(random.uniform(5.0, 10.0))
                dl_count = scrape_keyword(kw, disease_name, output_dir)
                total_downloaded += dl_count
                
    print(f"\n🎉 EXÉCUTION TERMINÉE ! Total des images téléchargées avec succès : {total_downloaded}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scraper multi-thread pour les images médicales")
    parser.add_argument("--csv", type=str, default="target_diseases.csv", help="Chemin vers le fichier CSV des maladies")
    parser.add_argument("--out", type=str, default="./dataset_images", help="Dossier de sortie principal")
    args = parser.parse_args()
    
    # Création du dossier principal si absent
    os.makedirs(args.out, exist_ok=True)
    
    main(args.csv, args.out)
